import typesystem


class WordForm(typesystem.Schema):
    value = typesystem.String(max_length=64)
    translate = typesystem.String(max_length=256, allow_blank=True)
