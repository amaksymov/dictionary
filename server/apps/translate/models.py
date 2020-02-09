from enum import Enum
from datetime import datetime

import orm

from server.apps.word.models import Word
from server.db import db, metadata
from server.utils.orm import fields
from server.utils.orm import models


class PartOfSpeechEnum(Enum):
    noun = 'noun'
    verb = 'verb'
    adjective = 'adjective'
    adverb = 'adverb'
    pronoun = 'pronoun'
    preposition = 'preposition'
    conjunction = 'conjunction'
    interjection = 'interjection'
    article = 'article'
    participle = 'participle'
    predicative = 'predicative'


class Translate(models.Model):
    __tablename__ = 'translates'
    __metadata__ = metadata
    __database__ = db

    id = orm.Integer(primary_key=True, index=True)
    created_date = orm.DateTime(default=datetime.now())
    word = orm.ForeignKey(Word)
    text = orm.String(max_length=256)
    part_of_speech = fields.Enum(PartOfSpeechEnum)
