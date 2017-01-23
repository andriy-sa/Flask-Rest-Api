import os

ORATOR_DATABASES = {
    'development': {
        'driver': 'postgres',
        'database': 'flask',
        'user': 'postgres',
        'password': '1',
        'host': '127.0.0.1',
        'port': '5432',
    }
}
APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = False
SECRET_KEY="c4623a202d5b4e47c9a28380c60de500d5815b78"
STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
WTF_CSRF_ENABLED = False
