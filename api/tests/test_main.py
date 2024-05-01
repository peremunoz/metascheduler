import os


def test_read_status(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "root": os.geteuid() == 0}
