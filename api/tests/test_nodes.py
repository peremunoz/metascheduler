import json


with open('config/test_config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
    test_nodes = config['cluster']['nodes']


def test_read_nodes(client):
    response = client.get('/cluster/nodes')
    assert response.status_code == 200
    assert len(response.json()) == len(test_nodes)
    for i, node in enumerate(test_nodes):
        assert response.json()[i]['id'] == i
        assert response.json()[i]['ip'] == node['ip']
        assert response.json()[i]['port'] == node['port']


def test_read_master_node(client):
    response = client.get('/cluster/nodes/master')
    assert response.status_code == 200
    assert response.json()['id'] == 0
    assert response.json()['ip'] == test_nodes[0]['ip']
    assert response.json()['port'] == test_nodes[0]['port']


def test_read_node(client):
    for i, node in enumerate(test_nodes):
        response = client.get(f'/cluster/nodes/{i}')
        assert response.status_code == 200
        assert response.json()['id'] == i
        assert response.json()['ip'] == node['ip']
        assert response.json()['port'] == node['port']
    response = client.get(f'/nodes/{len(test_nodes)}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'
