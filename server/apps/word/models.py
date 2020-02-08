from datetime import datetime

import orm

from server.apps.auth.models import User
from server.db import metadata, db
from server.utils.orm import models


class Word(models.Model):
    __tablename__ = 'words'
    __metadata__ = metadata
    __database__ = db

    id = orm.Integer(primary_key=True, index=True)
    value = orm.String(max_length=64, unique=True)
    created_date = orm.DateTime(default=datetime.now())
    repeat = orm.DateTime(default=datetime.now())
    done = orm.Boolean(default=False)
    user = orm.ForeignKey(User)
