import os


DEBUG = True

SECRET_KEY = 'Change me!!!'

INSTALLED_APPS = [
    'history_model',
    'poll',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
