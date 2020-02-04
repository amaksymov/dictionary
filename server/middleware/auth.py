from http import HTTPStatus

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import Response
from starlette.requests import Request
from starlette.applications import Starlette

from server.utils.session import Session
from server.utils.session.exceptions import SessionError


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Starlette):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        if raw_session := request.cookies.get('session'):
            try:
                user = await Session.get_user(raw_session)
            except SessionError as error:
                response = Response(
                    error.message,
                    status_code=HTTPStatus.BAD_REQUEST
                )
                Session.delete(response)
                return response
            request.scope['session'] = {'user_id': user.id}
            request.scope['user'] = user
        else:
            request.scope['session'] = {}
            request.scope['user'] = None

        response = await call_next(request)

        if user_id := request.session.get('user_id'):
            Session.set(str(user_id), response)
        else:
            Session.delete(response)
        return response
