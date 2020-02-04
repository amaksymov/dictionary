import databases
import orm
import sqlalchemy
from starlette.applications import Starlette

from server.settings import DATABASE_URI

db = databases.Database(DATABASE_URI)
metadata = sqlalchemy.MetaData()


def setup_db(app: Starlette):
    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
