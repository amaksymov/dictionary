from starlette.routing import Route

from server.apps.auth.github.views import login, callback


routes = [
    Route('/login', endpoint=login,
          methods=['POST'], name='login'),
    Route('/callback', endpoint=callback,
          methods=['GET'], name='callback'),
]
