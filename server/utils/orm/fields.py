import enum
import typing

import typesystem
import sqlalchemy
from sqlalchemy.dialects import postgresql
from orm.fields import ModelField


class Enum(ModelField, typesystem.Field):
    errors = {
        "value": "Not a valid {enum_cls.__name__}.",
    }

    def __init__(self, enum_cls: typing.Type[enum.Enum], **kwargs):
        super().__init__(**kwargs)
        self.enum_cls = enum_cls

    def validate(self, value, strict=False):
        try:
            return self.enum_cls(value)
        except ValueError:
            raise self.validation_error("value")

    def get_column_type(self):
        return sqlalchemy.Enum(self.enum_cls)


class UUID(ModelField, typesystem.String):
    def __init__(self, **kwargs):
        kwargs['format'] = 'uuid'
        super().__init__(**kwargs)

    def get_column_type(self):
        return postgresql.UUID(as_uuid=True)
