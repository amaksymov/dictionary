from typing import List, Optional
from http import HTTPStatus

import httpx
from starlette.exceptions import HTTPException

from server import settings
from server.apps.translate.models import Translate, PartOfSpeechEnum
from server.apps.word.models import Word


async def get_translate(word: Word) -> Optional[List[Translate]]:
    params = {
        'key': settings.YANDEX_DICTIONARY_KEY,
        'lang': 'en-ru',
        'text': word.value,
    }
    if settings.YANDEX_PROXY:
        proxies = {'https': settings.YANDEX_PROXY}
    else:
        proxies = {}
    async with httpx.AsyncClient(proxies=proxies) as client:
        resp = await client.get(settings.YANDEX_DICTIONARY_URL, params=params)
    if resp.status_code != HTTPStatus.OK:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR)
    payload = resp.json()
    translates = []
    if not payload['def']:
        return None
    for i in payload['def']:
        for tr in i['tr']:
            translate = Translate(
                part_of_speech=PartOfSpeechEnum(i['pos']),
                text=tr['text'],
            )
            translates.append(translate)

    return translates
