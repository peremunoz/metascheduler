test_job_1 = {
    "name": "job1",
    "queue": 1,
    "owner": "owner1"
}

test_job_2 = {
    "name": "job2",
    "queue": 1,
    "owner": "owner2"
}

test_job_3 = {
    "name": "job3",
    "queue": 2,
    "owner": "owner3"
}


def test_read_jobs_empty(client):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() == []


def test_create_job_one(client):
    response = client.post("/jobs", json=test_job_1)
    assert response.status_code == 201
    assert response.json() == {"status": "success",
                               "message": "Job created successfully"}
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == test_job_1["name"]
    assert response.json()[0]["queue"] == test_job_1["queue"]
    assert response.json()[0]["owner"] == test_job_1["owner"]


def test_create_job_many(client):
    response = client.post("/jobs", json=test_job_1)
    assert response.status_code == 201
    response = client.post("/jobs", json=test_job_2)
    assert response.status_code == 201
    response = client.post("/jobs", json=test_job_3)
    assert response.status_code == 201
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == test_job_1["name"]
    assert response.json()[0]["queue"] == test_job_1["queue"]
    assert response.json()[0]["owner"] == test_job_1["owner"]
    assert response.json()[1]["name"] == test_job_2["name"]
    assert response.json()[1]["queue"] == test_job_2["queue"]
    assert response.json()[1]["owner"] == test_job_2["owner"]
    assert response.json()[2]["name"] == test_job_3["name"]
    assert response.json()[2]["queue"] == test_job_3["queue"]
    assert response.json()[2]["owner"] == test_job_3["owner"]