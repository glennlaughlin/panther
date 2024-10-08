"""Generated by Panther."""
from datetime import timedelta
from pathlib import Path

from panther.utils import load_env

BASE_DIR = Path(__name__).resolve().parent
env = load_env(BASE_DIR / '.env')

MONITORING = True

LOG_QUERIES = True

# Load Env Variables
DB_NAME = env['DB_NAME']
DB_HOST = env['DB_HOST']
DB_PORT = env['DB_PORT']
SECRET_KEY = env['SECRET_KEY']
DB_USERNAME = env['DB_USERNAME']
DB_PASSWORD = env['DB_PASSWORD']

# # # More Info: https://pantherpy.github.io/middlewares/
MIDDLEWARES = [

]
"""
mongodb://[Username:Password(optional)]@HostName:Port/?aruguments
note: if your password has special characters, you would need to URL-Encode.

ex : mongodb://my-name:my-pass@localhost:27017/?authSource=users
"""
# # # More Info: Https://PantherPy.GitHub.io/authentications/
AUTHENTICATION = 'panther.authentications.JWTAuthentication'
WS_AUTHENTICATION = 'panther.authentications.QueryParamJWTAuthentication'

# Only If Authentication Set To JWT
JWTConfig = {
    'algorithm': 'HS256',
    'life_time': timedelta(days=2),
    'key': SECRET_KEY,
}

REDIS = {
    'class': 'panther.db.connections.RedisConnection',
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'websocket_db': 1,
}

DATABASE = {
    'engine': {
        # 'class': 'panther.db.connections.MongoDBConnection',
        'class': 'panther.db.connections.PantherDBConnection',
        # 'host': f'mongodb://{DB_HOST}:27017/{DB_NAME}'
    },
    # 'query': ...,
}

URLs = 'core.urls.urls'

USER_MODEL = 'app.models.User'

DEFAULT_CACHE_EXP = timedelta(seconds=10)

# THROTTLING = Throttling(rate=10, duration=timedelta(seconds=10))

# TEMPLATES_DIR = 'templates'


async def startup():
    print('Starting Up')


async def shutdown():
    print('Shutting Down')


STARTUP = 'core.configs.startup'
SHUTDOWN = 'core.configs.shutdown'

AUTO_REFORMAT = False

TIMEZONE = 'UTC'
