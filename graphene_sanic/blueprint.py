import copy
from collections import namedtuple
from sanic.blueprints import Blueprint as SanicBlueprint


FutureRoute = namedtuple('Route',
                         ['handler', 'uri',
                          'host', 'strict_slashes'])


DEPRECATED_METHODS = (
    'add_route', 'websocket',
    'add_websocket_route', 'get', 'post',
    'put', 'head', 'options', 'patch', 'delete'
)


BaseBluprint = copy.deepcopy(SanicBlueprint)

for method in DEPRECATED_METHODS:
    delattr(BaseBluprint, method)


class Blueprint(BaseBluprint):
    def register(self, app, options):
        """Register the blueprint to the sanic app."""

        url_prefix = options.get('url_prefix', self.url_prefix)

        # Routes
        for future in self.routes:
            # attach the blueprint name to the handler so that it can be
            # prefixed properly in the router
            future.handler.__blueprintname__ = self.name
            # Prepend the blueprint URI prefix if available
            uri = url_prefix + future.uri if url_prefix else future.uri
            app.route(
                uri=uri[1:] if uri.startswith('//') else uri,
                host=future.host or self.host,
                strict_slashes=future.strict_slashes
            )(future.handler)

        # Middleware
        for future in self.middlewares:
            if future.args or future.kwargs:
                app.register_middleware(future.middleware,
                                        *future.args,
                                        **future.kwargs)
            else:
                app.register_middleware(future.middleware)

        # Exceptions
        for future in self.exceptions:
            app.exception(*future.args, **future.kwargs)(future.handler)

        # Static Files
        for future in self.statics:
            # Prepend the blueprint URI prefix if available
            uri = url_prefix + future.uri if url_prefix else future.uri
            app.static(uri, future.file_or_directory,
                       *future.args, **future.kwargs)

        # Event listeners
        for event, listeners in self.listeners.items():
            for listener in listeners:
                app.listener(event)(listener)

    def route(self, uri, host=None, strict_slashes=False):
        def decorator(handler):
            route = FutureRoute(handler, uri, host, strict_slashes)
            self.routes.append(route)
            return handler
        return decorator
