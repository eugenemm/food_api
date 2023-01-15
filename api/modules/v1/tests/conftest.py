import pytest
import random

from manage import create_database, update_database, drop_database

@pytest.fixture(scope='session')
def prepare_test_db():
    create_database()
    try:
        update_database()
    except Exception as ex:
        pass
    yield None
    drop_database()


@pytest.fixture
def app():
    from modules import app
    return app
