import json
from api.routers.cluster import PutClusterModeModel
from api.constants.cluster_mode import ClusterMode

config_file = open("config/test_config.json", "r")
config = json.load(config_file)
test_cluster_mode = config['cluster']['mode']

root_put_cluster_mode_body: PutClusterModeModel = {
    "user": "root",
    "mode": ClusterMode.BEST_EFFORT.value
}

non_root_put_cluster_mode_body: PutClusterModeModel = {
    "user": "non_root",
    "mode": ClusterMode.BEST_EFFORT.value
}


def test_read_cluster_mode(client):
    response = client.get("/cluster/mode")
    assert response.status_code == 200
    assert response.json() == test_cluster_mode


def test_update_cluster_mode(client):
    response = client.get("/cluster/mode")
    assert response.status_code == 200
    assert response.json() == test_cluster_mode
    response = client.put("/cluster/mode", json=root_put_cluster_mode_body)
    assert response.status_code == 200
    assert response.json() == {"message": "Cluster mode updated"}
    response = client.get("/cluster/mode")
    assert response.status_code == 200
    assert response.json() == ClusterMode.BEST_EFFORT.value

    response = client.put("/cluster/mode", json=non_root_put_cluster_mode_body)
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
    response = client.get("/cluster/mode")
    assert response.status_code == 200
    assert response.json() == ClusterMode.BEST_EFFORT.value
