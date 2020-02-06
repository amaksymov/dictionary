from datetime import datetime
from http import HTTPStatus
from random import choice

from orm import NoMatch
from starlette.exceptions import HTTPException
from starlette.responses import Response, RedirectResponse
from starlette.requests import Request

from server.apps.learn.bl import get_next_repeat
from server.apps.learn.forms import ANSWERS
from server.apps.learn.models import AnswerHistory
from server.apps.word.models import Word
from server.utils.auth import LoginRequired
from server.utils import templates


@LoginRequired()
async def learn_word(request: Request) -> Response:
    now = datetime.now()
    words = await (
        Word.objects.filter(repeat__lte=now).all()
    )

    if words:
        word = choice(words)
    else:
        word = None
    return templates.TemplateResponse('learn/index.jinja2', {
        'word': word,
        'answers': ANSWERS,
        'request': request,
    })


@LoginRequired()
async def learned_word(request: Request) -> Response:
    word_id = request.path_params.get('word_id')

    try:
        word = await (
            Word.objects.filter(
                repeat__lte=datetime.now()
            )
            .get(id=word_id)
        )
    except NoMatch:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    if answer := request.path_params.get('answer'):
        if answer in map(lambda x: x.answer, ANSWERS):
            await AnswerHistory.objects.create(
                answer=answer,
                word=word,
            )
            answers = await (
                AnswerHistory.objects.filter(word__id=word.id).all()
            )
            repeat = get_next_repeat(answers)
            await word.update(
                repeat=repeat,
            )
    return RedirectResponse(
        request.url_for('learn:index'),
        status_code=HTTPStatus.MOVED_PERMANENTLY,
    )
