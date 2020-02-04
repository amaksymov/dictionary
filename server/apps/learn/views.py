from datetime import datetime
from http import HTTPStatus
from random import choice

from orm import NoMatch
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.requests import Request

from server.apps.learn.bl import get_next_repeat
from server.apps.learn.forms import LearnForm
from server.apps.learn.models import AnswerHistory
from server.apps.word.models import Word
from server.utils.response import redirect
from server.utils import templates, forms


async def learn_word(request: Request) -> Response:
    now = datetime.now()
    words = await (
        Word.objects.filter(repeat__lte=now).all()
    )

    if words:
        word = choice(words)
        from logging import warning
        warning(word)
        warning(word)
        warning(word)
        warning(word.repeat)
        warning(word)
    else:
        word = None

    return templates.TemplateResponse('learn/index.jinja2', {
        'word': word,
        'form': forms.Form(LearnForm),
        'request': request,
    })


async def learned_word(request: Request) -> Response:
    word_id = request.path_params.get('word_id')

    try:
        word = await Word.objects.get(id=word_id)
    except NoMatch:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    if request.method == 'POST':
        payload = await request.form()
        if answer := payload.get('answer'):
            if answer in ['0', '1', '2', '3', '4', '5']:
                await AnswerHistory.objects.create(
                    answer=int(answer),
                    word=word,
                )
                answers = await (
                    AnswerHistory.objects.filter(word__id=word.id).all()
                )
                repeat = get_next_repeat(answers)
                await word.update(
                    repeat=repeat,
                )
    return redirect(
        request.url_for('learn:index')
    )
