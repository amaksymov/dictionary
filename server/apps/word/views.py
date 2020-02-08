from typing import Dict
from http import HTTPStatus

from orm import NoMatch
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.exceptions import HTTPException

from server.apps.dictionary.bl import get_entity
from server.apps.dictionary.models import Entity
from server.apps.word.bl import create_word
from server.apps.translate.models import Translate, PartOfSpeechEnum
from server.utils.auth import LoginRequired
from server.utils import forms, templates
from server.apps.word.forms import WordForm
from server.apps.word.models import Word
from server.utils.bl.exception import BLException


@LoginRequired()
async def word_form(request: Request) -> Response:
    form = forms.Form(WordForm)
    errors: Dict[str, str] = {}

    words = await Word.objects.all()
    translates = await Translate.objects.filter(word__in=list(
        map(lambda x: x.id, words)
    )).all()
    dictionary = []
    for w in words:
        tr_text = {key: list() for key in PartOfSpeechEnum}
        for tr in filter(lambda x: x.word.pk == w.id, translates):
            tr_text[tr.part_of_speech].append(tr.text)
        dictionary.append(
            Entity(w, tr_text)
        )

    if request.method == 'POST':
        payload = await request.form()
        word_raw, word_errors = WordForm.validate_or_error({
            **payload,
        })
        if word_errors:
            form = forms.Form(WordForm, values=word_raw, errors=word_errors)
            return templates.TemplateResponse('index.jinja2', {
                'form': form,
                'dictionary': dictionary,
                'errors': errors,
                'request': request,
            })
        try:
            await create_word(word_raw, request.user)
            return RedirectResponse(
                request.url_for('index'),
                status_code=HTTPStatus.MOVED_PERMANENTLY,
            )
        except BLException as error:
            errors[error.code] = error.message
        return templates.TemplateResponse('index.jinja2', {
            'form': form,
            'dictionary': dictionary,
            'errors': errors,
            'request': request,
        })

    return templates.TemplateResponse('index.jinja2', {
        'form': form,
        'dictionary': dictionary,
        'errors': errors,
        'request': request,
    })


@LoginRequired()
async def word_detail(request: Request) -> Response:
    word_id = request.path_params.get('word_id')
    if not word_id:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    try:
        word = await Word.objects.get(id=word_id)
        if word.user.pk != request.user.id:
            raise NoMatch
    except NoMatch:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    translates = await Translate.objects.filter(word__id=word.id).all()
    entity = get_entity(word, translates)

    return templates.TemplateResponse('word/detail.jinja2', {
        'entity': entity,
        'request': request,
    })


@LoginRequired()
async def word_delete(request: Request) -> Response:
    if request.method == 'POST':
        word_id = request.path_params.get('word_id')
        try:
            word = await Word.objects.get(id=word_id)
            if word.user.pk != request.user.id:
                raise NoMatch
        except NoMatch:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        await word.delete()
    return RedirectResponse(
        request.url_for('index'),
        status_code=HTTPStatus.MOVED_PERMANENTLY,
    )


@LoginRequired()
async def word_create(request: Request) -> Response:
    form = forms.Form(WordForm)
    errors = {}

    if request.method == 'POST':
        payload = await request.form()
        word_raw, word_errors = WordForm.validate_or_error({
            **payload,
        })
        if word_errors:
            form = forms.Form(WordForm, values=word_raw, errors=word_errors)
            return templates.TemplateResponse('word/create.jinja2', {
                'form': form,
                'errors': errors,
                'request': request,
            })
        try:
            await create_word(word_raw, request.user)
            return RedirectResponse(
                url=request.url_for('index'),
                status_code=HTTPStatus.MOVED_PERMANENTLY,
            )
        except BLException as error:
            errors[error.code] = error.message

    return templates.TemplateResponse('word/create.jinja2', {
        'form': form,
        'errors': errors,
        'request': request,
    })
