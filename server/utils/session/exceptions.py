from typing import Any, Tuple


class SessionError(Exception):
    def __init__(self, message: str, *args: Tuple[Any]) -> None:
        self.message = message
        super().__init__(*args)
