from datetime import datetime

import orm

from server.db import metadata, db
from server.apps.word.models import Word


class AnswerHistory(orm.Model):
    __tablename__ = 'answer_history'
    __metadata__ = metadata
    __database__ = db

    id = orm.Integer(primary_key=True, index=True)
    answer = orm.Integer()
    created_date = orm.DateTime(default=datetime.now())
    word = orm.ForeignKey(Word)
