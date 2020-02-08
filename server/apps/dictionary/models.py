from dataclasses import dataclass
from typing import List, Dict

from server.apps.translate.models import Translate, PartOfSpeechEnum
from server.apps.word.models import Word


@dataclass
class Entity:
    word: Word
    translates: Dict[PartOfSpeechEnum, List[str]]

    def __iter__(self):
        yield self.word
        yield self.translates
