from http import HTTPStatus

from starlette.responses import RedirectResponse


def redirect(url: str, status_code: int = HTTPStatus.TEMPORARY_REDIRECT):
    return RedirectResponse(
        url=url,
        status_code=status_code,
    )
