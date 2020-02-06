from http import HTTPStatus

from starlette.responses import Response, RedirectResponse
from starlette.requests import Request

from server.utils import templates


async def logout(request: Request) -> Response:
    request.session.clear()
    url = request.url_for('index')
    return RedirectResponse(url, status_code=HTTPStatus.SEE_OTHER)


async def login_page(request: Request) -> Response:
    # TODO: Add redirect next_url
    # next_url = request.query_params.get('next_url')
    return templates.TemplateResponse('auth/login_page.jinja2', {
        'request': request,
    })
