# Graphene-Sanic

The combination of [sanic](https://github.com/channelcat/sanic) and [graphene](https://github.com/graphql-python/graphene)

## Hello World Example

``` python

from graphene import *
from graphene_sanic import GrapheneSanic
from graphene_sanic.view import View


app = GrapheneSanic(__name__, websocket_enabled=True)


@app.route("/")
class Query(View):
    hello = String(name=Argument(String, default_value="stranger"))

    def resolve_hello(self, args, context, info):
        return 'World'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


```

## Final Thoughts

                     ▄▄▄▄▄
            ▀▀▀██████▄▄▄       _______________
          ▄▄▄▄▄  █████████▄  /                 \
         ▀▀▀▀█████▌ ▀▐▄ ▀▐█ |   Gotta go fast!  |
       ▀▀█████▄▄ ▀██████▄██ | _________________/
       ▀▄▄▄▄▄  ▀▀█▄▀█════█▀ |/
            ▀▀▀▄  ▀▀███ ▀       ▄▄
         ▄███▀▀██▄████████▄ ▄▀▀▀▀▀▀█▌
       ██▀▄▄▄██▀▄███▀ ▀▀████      ▄██
    ▄▀▀▀▄██▄▀▀▌████▒▒▒▒▒▒███     ▌▄▄▀
    ▌    ▐▀████▐███▒▒▒▒▒▐██▌
    ▀▄▄▄▄▀   ▀▀████▒▒▒▒▄██▀
              ▀▀█████████▀
            ▄▄██▀██████▀█
          ▄██▀     ▀▀▀  █
         ▄█             ▐▌
     ▄▄▄▄█▌              ▀█▄▄▄▄▀▀▄
    ▌     ▐                ▀▀▄▄▄▀
     ▀▀▄▄▀
