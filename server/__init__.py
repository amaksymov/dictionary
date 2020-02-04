from starlette.applications import Starlette

from server.db import setup_db
from server.routes import setup_routes
from server.settings import DEBUG
from server.middleware import setup_middleware

__version__ = '0.1.0'


def create_app() -> Starlette:
    app = Starlette(
        debug=DEBUG,
    )

    setup_db(app)
    setup_routes(app)
    setup_middleware(app)

    return app
