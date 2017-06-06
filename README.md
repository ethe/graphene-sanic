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
    hello = String()

    def resolve_hello(self, args, context, info):
        return 'world'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

```

Then try to execute `curl '127.0.0.1:5000/?query=\{hello\}'` and get response!

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
