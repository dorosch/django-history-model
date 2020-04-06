import pytest
from django import conf
from django.db import connection


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


@pytest.fixture(scope='function')
def db_tables():
    return connection.introspection.table_names()


@pytest.fixture(scope='function')
def model():
    from .models import MyModel
    return MyModel


@pytest.fixture(scope='function')
def history_model(model):
    return model.history.model
