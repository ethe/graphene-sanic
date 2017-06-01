try:
    from ujson import dumps
except:
    from json import dumps
from graphene import ObjectType, Schema
from sanic.response import json
from sanic.exceptions import ServerError


class View(ObjectType):

    decorators = []

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        cls = self.__class__
        if not hasattr(cls, 'schema'):
            cls.schema = Schema(query=cls)
        self.__name__ = cls.__name__

    async def get(self, request, ws=None):
        if not ws:
            try:
                query = request.args['query']
            except KeyError:
                raise ServerError(
                    "need parameter 'query' for get method", status_code=403)
            return json(self.schema.execute(query[0]))
        else:
            while True:
                data = await ws.recv()
                await ws.send(dumps(self.schema.execute(data)))

    async def post(self, request, ws=None):
        query = request.body.replace(b'\n', b'').decode('utf8')

        return json(self.schema.execute(query))

    def _dispatch_request(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), None)
        return handler(request, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Return view function for use with the routing system, that
        dispatches request to appropriate handler method.
        """
        def view(*args, **kwargs):
            return self._dispatch_request(*args, **kwargs)

        if self.decorators:
            for decorator in self.decorators:
                view = decorator(view)
        return view(*args, **kwargs)
