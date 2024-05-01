import json


config_file = open("config/test.config", "r")
config = json.load(config_file)
test_nodes = config['cluster']['nodes']


def test_read_nodes(client):
    response = client.get("/nodes")
    assert response.status_code == 200
    assert len(response.json()) == len(test_nodes)
    for i in range(len(test_nodes)):
        assert response.json()[i]['id'] == i
        assert response.json()[i]['ip'] == test_nodes[i]['ip']
        assert response.json()[i]['port'] == test_nodes[i]['port']
        assert response.json()[i]['is_alive'] == False or True or None


def test_read_master_node(client):
    response = client.get("/nodes/master")
    assert response.status_code == 200
    assert response.json()['id'] == 0
    assert response.json()['ip'] == test_nodes[0]['ip']
    assert response.json()['port'] == test_nodes[0]['port']
    assert response.json()['is_alive'] == False or True or None


def test_read_node(client):
    for i in range(len(test_nodes)):
        response = client.get(f"/nodes/{i}")
        assert response.status_code == 200
        assert response.json()['id'] == i
        assert response.json()['ip'] == test_nodes[i]['ip']
        assert response.json()['port'] == test_nodes[i]['port']
        assert response.json()['is_alive'] == False or True or None
    response = client.get(f"/nodes/{len(test_nodes)}")
    assert response.status_code == 404
    assert response.json()['detail'] == "Node not found"