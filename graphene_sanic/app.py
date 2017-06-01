import copy
from asyncio import ensure_future, CancelledError
from websockets import InvalidHandshake
from sanic.exceptions import InvalidUsage

from sanic import Sanic
from sanic.config import LOGGING
from sanic.constants import HTTP_METHODS
from sanic.websocket import ConnectionClosed


DEPRECATED_METHODS = (
    'get', 'post', 'put', 'head',
    'options', 'patch', 'delete', 'add_route',
    'websocket', 'add_websocket_route', 'enable_websocket'
)


BaseApp = copy.deepcopy(Sanic)

for method in DEPRECATED_METHODS:
    delattr(BaseApp, method)


class GrapheneSanic(BaseApp):

    def __init__(self, name=None, router=None, error_handler=None,
                 load_env=True, request_class=None,
                 log_config=LOGGING, websocket_enabled=False):
        super(GrapheneSanic, self).__init__(
            name=None, router=None, error_handler=None,
            load_env=True, request_class=None,
            log_config=LOGGING
        )
        self.websocket_enabled = websocket_enabled
        if websocket_enabled:
            self.websocket_quit_listener()

    # Decorator
    def route(self, uri, host=None,
              strict_slashes=False, args=[], kwargs={}):
        # Fix case where the user did not prefix the URL with a /
        # and will probably get confused as to why it's not working
        if not uri.startswith('/'):
            uri = '/' + uri

        def response(handler_class):
            custom_handler = handler_class(*args, **kwargs)

            if not self.websocket_enabled:
                handler = custom_handler
            else:
                async def handler(request, *args, **kwargs):
                    request.app = self
                    try:
                        protocol = request.transport.get_protocol()
                    except AttributeError:
                        # On Python3.5 the Transport classes in asyncio do not
                        # have a get_protocol() method as in uvloop
                        protocol = request.transport._protocol
                    try:
                        ws = await protocol.websocket_handshake(request)
                    except (InvalidHandshake, InvalidUsage):
                        # not websocket protocol, try to use standard http protocol
                        res = await custom_handler(request, ws=None, *args, **kwargs)
                        return res

                    # schedule the application handler
                    # its future is kept in self.websocket_tasks in case it
                    # needs to be cancelled due to the server being stopped
                    fut = ensure_future(custom_handler(request, ws, *args, **kwargs))
                    self.websocket_tasks.append(fut)
                    try:
                        await fut
                    except (CancelledError, ConnectionClosed):
                        pass
                    self.websocket_tasks.remove(fut)
                    await ws.close()

            methods = set()
            for method in HTTP_METHODS:
                if getattr(handler, method.lower(), None):
                    methods.add(method)

            self.router.add(uri=uri, methods=methods, handler=handler,
                            host=host, strict_slashes=strict_slashes)
            return handler

        return response

    def websocket_quit_listener(self):
        # if the server is stopped, we want to cancel any ongoing
        # websocket tasks, to allow the server to exit promptly
        @self.listener('before_server_stop')
        def cancel_websocket_tasks(app, loop):
            for task in self.websocket_tasks:
                task.cancel()
