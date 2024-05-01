from fastapi.testclient import TestClient
from api.main import app
import json

client = TestClient(app)

config_file = open("config/test.config", "r")
config = json.load(config_file)
test_nodes = config['cluster']['nodes']


def test_read_nodes():
    response = client.get("/nodes")
    assert response.status_code == 200
    assert len(response.json()) == len(test_nodes)
    for i in range(len(test_nodes)):
        assert response.json()[i]['id'] == i
        assert response.json()[i]['ip'] == test_nodes[i]['ip']
        assert response.json()[i]['port'] == test_nodes[i]['port']
        assert response.json()[i]['is_alive'] == False or True or None
