from graphene import *
from graphene_sanic import GrapheneSanic
from graphene_sanic.view import View
from graphene_sanic.blueprint import Blueprint


app = GrapheneSanic(__name__, websocket_enabled=True)


bp = Blueprint('my_blueprint', url_prefix='/test')


@bp.route("/")
class Query(View):
    hello = String(name=Argument(String, default_value="stranger"))

    def resolve_hello(self, args, context, info):
        return 'Hello ' + args['name']


if __name__ == '__main__':
    app.blueprint(bp)
    app.run(host="0.0.0.0", port=5000)
