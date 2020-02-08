import typesystem


class WordForm(typesystem.Schema):
    value = typesystem.String(max_length=64)
