import orm
import typesystem


class Model(orm.Model):
    __abstract__ = True

    async def save(self) -> None:
        # Validate the keyword arguments.
        fields = self.fields
        required = [key for key, value in fields.items() if not value.has_default()]
        validator = typesystem.Object(
            properties=fields, required=required, additional_properties=False
        )
        kwargs = validator.validate(self.__dict__)

        # Remove primary key when None to prevent not null constraint in postgresql.
        pkname = self.__pkname__
        pk = self.fields[pkname]
        if kwargs[pkname] is None and pk.allow_null:
            del kwargs[pkname]

        # Build the insert expression.
        expr = self.__table__.insert()
        expr = expr.values(**kwargs)

        # Execute the insert, and return a new model instance.
        self.pk = await self.__database__.execute(expr)
