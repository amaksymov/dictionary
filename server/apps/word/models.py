from datetime import datetime

import orm

from server.db import metadata, db


class Word(orm.Model):
    __tablename__ = 'words'
    __metadata__ = metadata
    __database__ = db

    id = orm.Integer(primary_key=True, index=True)
    value = orm.String(max_length=64, unique=True)
    translate = orm.String(max_length=256, allow_null=True)
    created_date = orm.DateTime(default=datetime.now())
    repeat = orm.DateTime(default=datetime.now())
    done = orm.Boolean(default=False)
