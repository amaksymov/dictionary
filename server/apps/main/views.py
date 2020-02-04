from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from server.utils import templates


async def index(request: Request) -> Response:
    return templates.TemplateResponse('index.jinja2', {
        'request': request,
    })


async def status(request: Request) -> Response:
    return JSONResponse({'status': 'ok'})
