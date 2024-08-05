import pytest
from page_analyzer.app import app


@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update({'TESTING': True})
    # other setup can go here
    yield test_app
    # clean up / reset resources here


@pytest.fixture()
def client(test_app):
    return app.test_client()


@pytest.fixture()
def runner(test_app):
    return app.test_cli_runner()
