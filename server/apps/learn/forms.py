from dataclasses import dataclass
from enum import Enum


class ButtonType(Enum):
    primary = 'primary'
    secondary = 'secondary'
    success = 'success'
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    light = 'light'
    dark = 'dark'
    link = 'link'


@dataclass
class Answer:
    answer: int
    text: str
    btn_type: ButtonType


ANSWERS = [
    Answer(0, 'Incorrect, Hardest', ButtonType.danger),
    Answer(1, 'Incorrect, Hard', ButtonType.secondary),
    Answer(2, 'Incorrect, Medium', ButtonType.warning),
    Answer(3, 'Correct, Medium', ButtonType.primary),
    Answer(4, 'Correct, Easy', ButtonType.info),
    Answer(5, 'Correct, Easiest', ButtonType.success),
]
