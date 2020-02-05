from starlette.datastructures import URL
from starlette.requests import Request

from server.utils.response import redirect


class LoginRequired:
    def __init__(self, admin_only: bool = False):
        self.admin_only = admin_only

    def __call__(self, f):
        async def wrapped_f(request: Request, *args, **kwargs):
            if request.user:
                if not self.admin_only or request.user.is_admin:
                    return await f(request, *args, **kwargs)
            redirect_url = URL(
                request.url_for('auth:login_page')
            ).include_query_params(next_url=request.scope['path'])
            return redirect(
                url=str(redirect_url),
            )
        return wrapped_f
