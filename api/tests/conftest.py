import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture
def client():
    """Create a FastAPI test client"""
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test (delete sqlite file)"""
    from api.utils.DatabaseHelper import DatabaseHelper
    DatabaseHelper().reset_database_for_testing()
