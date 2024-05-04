import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.utils.database_helper import DatabaseHelper


@pytest.fixture
def client():
    '''Create a FastAPI test client'''
    with TestClient(app):
        yield TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    '''Reset the database before each test (delete sqlite file)'''
    DatabaseHelper().reset_database_for_testing()
