from django import conf


def pytest_configure():
    conf.settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SECRET_KEY='not need secret key in tests',
        ROOT_URLCONF=[],
        INSTALLED_APPS=(
            'tests',
            'history_model'
        )
    )
