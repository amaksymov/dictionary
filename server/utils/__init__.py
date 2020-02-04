import typesystem
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


templates = Jinja2Templates(directory='server/templates')

forms = typesystem.Jinja2Forms(package='bootstrap4')
static_files = StaticFiles(directory='server/static', packages=["bootstrap4"])

