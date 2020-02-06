from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router

from server.apps.word.views import (
    word_form,
    word_edit,
    word_delete,
    word_create,
)
from server.apps.auth.routes import routes as auth_routes
from server.apps.learn.views import learn_word, learned_word
from server.apps.main.views import status
from server.utils import static_files


def setup_routes(app: Starlette):
    app.mount('/', Router([
        Route('/', endpoint=word_form, methods=['GET', 'POST'], name='index'),
        Route('/', endpoint=learn_word, methods=['GET'], name='learn'),
        Mount('/learn', name='learn', app=Router([
            Route('/', endpoint=learn_word,
                  methods=['GET'], name='index'),
            Route('/{word_id:int}/{answer:int}', endpoint=learned_word,
                  methods=['GET'], name='learned'),
        ])),
        Mount('/w', name='word', app=Router([
            Route('/create', endpoint=word_create,
                  methods=['GET', 'POST'], name='create'),
            Route('/{word_id:int}/edit', endpoint=word_edit,
                  methods=['GET', 'POST'], name='edit'),
            Route('/{word_id:int}/delete', endpoint=word_delete,
                  methods=['POST'], name='delete'),
        ])),

        # Auth
        Mount('/auth', name='auth', app=Router([
            *auth_routes
        ])),

        # API
        Mount('/api', app=Router([
            Mount('/v1', app=Router([
                Mount('/status', app=Router([
                    Route('/', endpoint=status,
                          methods=['GET']),
                ])),
            ])),
        ])),
        Mount('/static', static_files, name='static'),
    ]))
