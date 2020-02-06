import datetime
from http import HTTPStatus

import httpx
from orm import NoMatch
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.datastructures import URL

from server import settings
from server.apps.auth.models import User


async def login(request: Request) -> Response:
    query = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'redirect_url': request.url_for('auth:github:callback'),
    }
    url = URL(settings.GITHUB_AUTH_URL).include_query_params(**query)
    return RedirectResponse(url, status_code=HTTPStatus.SEE_OTHER)


async def callback(request):
    github_client = httpx.AsyncClient(base_url=settings.GITHUB_URL)
    github_api_client = httpx.AsyncClient(
        base_url=settings.GITHUB_API_URL,
        headers={'accept': 'application/vnd.github.v3+json'}
    )

    # Obtain an access token.
    code = request.query_params.get('code', '')
    url = '/login/oauth/access_token'
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
    }
    headers = {'accept': 'application/json'}
    response = await github_client.post(url, data=data, headers=headers)
    response.raise_for_status()
    data = response.json()

    #  Make a request to the API.
    url = '/user'
    headers = {
        'authorization': f'token {data["access_token"]}',
    }
    response = await github_api_client.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Log the user in, and redirect back to the homepage.
    try:
        user = await User.objects.get(github_id=data['id'])
        values = {
            'last_login': datetime.datetime.now(),
            'username': data['login'],
            'name': data['name'],
            'avatar_url': data['avatar_url'],
        }
        user.update(**values)
    except NoMatch:
        values = {
            'username': data['login'],
            'github_id': data['id'],
            'is_admin': True,
            'avatar_url': data['avatar_url'],
        }
        user = await User.objects.create(**values)

    request.scope['user'] = user
    request.scope['session']['user_id'] = user.id
    url = request.url_for('index')
    return RedirectResponse(url, status_code=HTTPStatus.SEE_OTHER)
