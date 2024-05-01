from fastapi.testclient import TestClient
import os
from api.main import app

client = TestClient(app)


def test_read_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "root": os.geteuid() == 0}
