import os
from base64 import encodebytes
from datetime import timedelta

ORATOR_DATABASES = {
    'default': 'mysql',
    'main': {
        'driver': 'postgres',
        'database': 'flask',
        'user': 'postgres',
        'password': '1',
        'host': '127.0.0.1',
        'port': '5432',
    },
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'silverdeer_flask',
        'user': 'root',
        'password': '1',
        'prefix': ''
    },
    'testing': {
        'driver': 'postgres',
        'database': 'test_flask',
        'user': 'postgres',
        'password': '1',
        'host': '127.0.0.1',
        'port': '5432',
    }
}
APPLICATION_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEBUG = True
SECRET_KEY = "c4623a202d5b4e47c9a28380c60de500d5815b78"
STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
WTF_CSRF_ENABLED = False
ELASTICSEARCH_HTTP_AUTH = 'es_admin:141294'
JWT_AUTH_URL_RULE = '/api/auth'
JWT_AUTH_USERNAME_KEY = 'email'
JWT_EXPIRATION_DELTA = timedelta(days=30)
