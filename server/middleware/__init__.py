from starlette.applications import Starlette

from server.middleware.auth import AuthMiddleware


def setup_middleware(app: Starlette) -> None:
    app.add_middleware(AuthMiddleware)
