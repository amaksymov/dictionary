from starlette.routing import Mount, Route, Router

from server.apps.auth.github.routes import routes as github_routes
from server.apps.auth.views import logout, login_page


routes = [
    Mount('/github', name='github', app=Router([
        *github_routes
    ])),
    Route('/login-required', endpoint=login_page,
          methods=['GET'], name='login_page'),
    Route('/logout', endpoint=logout,
          methods=['POST'], name='logout'),
]
