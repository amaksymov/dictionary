import typesystem


class LearnForm(typesystem.Schema):
    answer = typesystem.Choice(title="Answer", choices=[
        ('0', 'Incorrect, Hardest'),
        ('1', 'Incorrect, Hard'),
        ('2', 'Incorrect, Medium'),
        ('3', 'Correct, Medium'),
        ('4', 'Correct, Easy'),
        ('5', 'Correct, Easiest'),
    ])
