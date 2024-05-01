import json

config_file = open("config/test.config", "r")
config = json.load(config_file)
test_cluster_mode = config['cluster']['mode']


def test_read_cluster_mode(client):
    response = client.get("/cluster/mode")
    assert response.status_code == 200
    assert response.json() == test_cluster_mode
