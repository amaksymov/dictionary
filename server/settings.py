from starlette.config import Config

config = Config('.env')

DATABASE_URI = config('DATABASE_URI', cast=str)
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=str)
HTTPS_ONLY = config('HTTPS_ONLY', cast=str, default=False)

SESSION_MAX_AGE = config('SESSION_MAX_AGE', cast=int, default=5 * 24 * 60 * 60)
SESSION_NAME = config('SESSION_NAME', cast=str, default='session')

GITHUB_URL = config('GITHUB_URL', cast=str, default='https://github.com/')
GITHUB_API_URL = config('GITHUB_API_URL', cast=str,
                        default='https://api.github.com/')
GITHUB_AUTH_URL = config('GITHUB_AUTH_URL', cast=str,
                         default='https://github.com/login/oauth/authorize')
GITHUB_CLIENT_ID = config('GITHUB_CLIENT_ID', cast=str)
GITHUB_CLIENT_SECRET = config('GITHUB_CLIENT_SECRET', cast=str)
