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
    import os
    if os.path.exists("db/test_db.sqlite3"):
        os.remove("db/test_db.sqlite3")
    yield
    if os.path.exists("db/test_db.sqlite3"):
        os.remove("db/test_db.sqlite3")
