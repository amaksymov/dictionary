from typing import List

from server.apps.dictionary.models import Entity
from server.apps.translate.models import Translate, PartOfSpeechEnum
from server.apps.word.models import Word


def get_entity(word: Word, translates: List[Translate]) -> Entity:
    tr_text = {key: list() for key in PartOfSpeechEnum}
    for tr in translates:
        tr_text[tr.part_of_speech].append(tr.text)
    return Entity(
        word,
        translates=tr_text,
    )
