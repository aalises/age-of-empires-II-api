import pytest
from api import create_app
from config import APP_CONFIG

@pytest.fixture
def app():
    APP_CONFIG.update({'TESTING': True})
    app = create_app(APP_CONFIG)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
