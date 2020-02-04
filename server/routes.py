from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router

from server.apps.word.views import (
    word_form,
    word_edit,
    word_delete,
    word_create,
)
from server.apps.auth.views import login, logout, callback
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
            Route('/{word_id:int}', endpoint=learned_word,
                  methods=['POST'], name='learned'),
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
            Route('/login', endpoint=login,
                  methods=['POST'], name='login'),
            Route('/logout', endpoint=logout,
                  methods=['POST'], name='logout'),
            Route('/callback', endpoint=callback,
                  methods=['GET'], name='callback'),
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
