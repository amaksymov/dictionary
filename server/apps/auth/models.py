from datetime import datetime

import orm

from server.db import metadata, db


class User(orm.Model):
    __tablename__ = 'users'
    __metadata__ = metadata
    __database__ = db

    id = orm.Integer(primary_key=True, index=True)
    github_id = orm.Integer(index=True)
    username = orm.String(max_length=256)
    last_login = orm.DateTime(default=datetime.now())
    created_date = orm.DateTime(default=datetime.now())
    avatar_url = orm.String(allow_null=True, max_length=256)
    is_admin = orm.Boolean(default=False)
