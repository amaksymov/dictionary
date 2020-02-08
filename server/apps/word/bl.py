from typing import Optional

import asyncpg

from server.apps.auth.models import User
from server.apps.dictionary.bl import get_entity
from server.apps.dictionary.models import Entity
from server.apps.translate.client import get_translate
from server.apps.word.forms import WordForm
from server.apps.word.models import Word
from server.utils.bl.exception import BLException


async def create_word(word_raw: WordForm, user: User) -> Entity:
    fields = dict(**word_raw)
    fields['value'] = fields['value'].lower()
    word = Word(
        **fields,
        user=user
    )
    translates = await get_translate(word)
    if not translates:
        raise BLException('Translate not found', 'translate')
    try:
        await word.save()
    except asyncpg.exceptions.UniqueViolationError:
        raise BLException('Word already exists in your dictionary', 'duplicate')

    for tr in translates:
        tr.word = word
        await tr.save()
    return get_entity(word, translates)

