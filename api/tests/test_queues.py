import json
from typing import List

with open("config/test_config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    schedulers = config['cluster']['schedulers']

queues_names: List[str] = []
for scheduler in schedulers:
    queues_names.append(scheduler['name'])


def test_read_queues(client):
    response = client.get("/queues")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "scheduler_name": queues_names[0]},
        {"id": 2, "scheduler_name": queues_names[1]},
    ]
