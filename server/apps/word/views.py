from http import HTTPStatus

from orm import NoMatch
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException

from server.utils.response import redirect
from server.utils import forms, templates
from server.apps.word.forms import WordForm
from server.apps.word.models import Word


async def word_form(request: Request) -> Response:
    form = forms.Form(WordForm)
    errors = {}

    words = await Word.objects.all()

    if request.method == 'POST':
        payload = await request.form()
        word_raw, word_errors = WordForm.validate_or_error({
            **payload,
        })
        if word_errors:
            form = forms.Form(WordForm, values=word_raw, errors=word_errors)
            return templates.TemplateResponse('index.jinja2', {
                'form': form,
                'words': words,
                'errors': errors,
                'request': request,
            })
        await Word.objects.create(**word_raw)
        return redirect(
            url=request.url_for('index'),
        )

    return templates.TemplateResponse('index.jinja2', {
        'form': form,
        'words': words,
        'errors': errors,
        'request': request,
    })


async def word_edit(request: Request) -> Response:
    errors = {}
    is_editing = True

    word_id = request.path_params.get('word_id')
    if not word_id:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    try:
        word = await Word.objects.get(id=word_id)
    except NoMatch:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    form = forms.Form(WordForm, values={'value': word.value, 'translate': word.translate})

    if request.method == 'POST':
        payload = await request.form()
        word_raw, word_errors = WordForm.validate_or_error({
            **payload,
        })
        if word_errors:
            form = forms.Form(WordForm, values=word_raw, errors=word_errors)
            return templates.TemplateResponse('word/form.jinja2', {
                'form': form,
                'word': word,
                'is_editing': is_editing,
                'errors': errors,
                'request': request,
            })
        await word.update(**word_raw)
        return redirect(
            request.url_for('word:edit', word_id=word.id)
        )

    return templates.TemplateResponse('word/form.jinja2', {
        'form': form,
        'word': word,
        'is_editing': is_editing,
        'errors': errors,
        'request': request,
    })


async def word_delete(request: Request) -> Response:
    if request.method == 'POST':
        word_id = request.path_params.get('word_id')
        try:
            word = await Word.objects.get(id=word_id)
        except NoMatch:
            raise HTTPException(HTTPStatus.NOT_FOUND)
        await word.delete()
    return redirect(
        request.url_for('index')
    )


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
        await Word.objects.create(**word_raw)
        return redirect(
            url=request.url_for('index'),
        )

    return templates.TemplateResponse('word/create.jinja2', {
        'form': form,
        'errors': errors,
        'request': request,
    })
