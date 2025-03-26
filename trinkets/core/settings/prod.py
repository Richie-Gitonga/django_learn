from .base import *

DEBUG = False
ADMINS = [
    ('Richie M', 'gitongar00@gmail.com'),
]

ALLOWED_HOSTS = ['*']
DATABASES  = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}