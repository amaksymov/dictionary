import logging
from itsdangerous import TimestampSigner, exc
from orm import NoMatch
from starlette.responses import Response

from server.apps.auth.models import User
from server.settings import SECRET_KEY, SESSION_MAX_AGE, SESSION_NAME
from server.utils.session.exceptions import SessionError

log = logging.getLogger()

ENCODING = 'UTF-8'


class Session:
    class Meta:
        s = TimestampSigner(SECRET_KEY)
        name = SESSION_NAME
        max_age = SESSION_MAX_AGE

    @classmethod
    def set(cls, user_id: str, response: Response) -> None:
        payload = cls.sign(user_id)
        response.set_cookie(
            cls.Meta.name,
            payload,
            expires=cls.Meta.max_age,
            httponly=True,
        )

    @classmethod
    async def get_user(cls, raw_session: str) -> User:
        try:
            user_id = int(cls.unsign(raw_session))
            user = await User.objects.get(id=user_id)
        except NoMatch as error:
            log.error(error)
            raise SessionError('Session invalid')
        except exc.BadTimeSignature as error:
            log.error(error)
            raise SessionError(error.message)
        return user

    @classmethod
    def delete(cls, response: Response):
        response.delete_cookie(cls.Meta.name)

    @classmethod
    def sign(cls, user_id: str):
        return cls.Meta.s.sign(user_id).decode(ENCODING)

    @classmethod
    def unsign(cls, value: str):
        return cls.Meta.s.unsign(value, max_age=cls.Meta.max_age)

