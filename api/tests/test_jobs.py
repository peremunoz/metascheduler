from api.constants.job_status import JobStatus
from api.routers.jobs import PostJobModel

test_job_1: PostJobModel = {
    'name': 'job1',
    'queue': 1,
    'owner': 'owner1',
    'path': '/path/to/job1',
    'options': '--option1 value1 --option2 value2'
}

test_job_2: PostJobModel = {
    'name': 'job2',
    'queue': 1,
    'owner': 'owner2',
    'path': '/path/to/job2',
    'options': '--option1 value1 --option2 value2'
}

test_job_3: PostJobModel = {
    'name': 'job3',
    'queue': 2,
    'owner': 'owner3',
    'path': '/path/to/job3',
    'options': '--option1 value1 --option2 value2'
}

test_job_4_no_options: PostJobModel = {
    'name': 'job4',
    'queue': 2,
    'owner': 'owner4',
    'path': '/path/to/job4'
}


def test_read_jobs_empty(client):
    response = client.get('/jobs', params={'owner': 'root'})
    assert response.status_code == 200
    assert response.json() == []


def test_create_job_one(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    assert response.json() == {'status': 'success',
                               'message': 'Job created successfully ✅'}

    response = client.get('/jobs', params={'owner': 'root'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[0]['path'] == test_job_1['path']
    assert response.json()[0]['options'] == test_job_1['options']


def test_create_job_many(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get('/jobs', params={'owner': 'root'})
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[0]['path'] == test_job_1['path']
    assert response.json()[0]['options'] == test_job_1['options']
    assert response.json()[1]['name'] == test_job_2['name']
    assert response.json()[1]['queue'] == test_job_2['queue']
    assert response.json()[1]['owner'] == test_job_2['owner']
    assert response.json()[1]['path'] == test_job_2['path']
    assert response.json()[1]['options'] == test_job_2['options']
    assert response.json()[2]['name'] == test_job_3['name']
    assert response.json()[2]['queue'] == test_job_3['queue']
    assert response.json()[2]['owner'] == test_job_3['owner']
    assert response.json()[2]['path'] == test_job_3['path']
    assert response.json()[2]['options'] == test_job_3['options']


def test_create_job_invalid_queue(client):
    response = client.post(
        '/jobs', json={**test_job_1, 'queue': 3})
    assert response.status_code == 500
    assert response.json() == {'detail': 'Queue 3 not found'}


def test_read_jobs_by_owner(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get('/jobs', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[0]['path'] == test_job_1['path']
    assert response.json()[0]['options'] == test_job_1['options']

    response = client.get('/jobs', params={'owner': 'owner2'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_2['name']
    assert response.json()[0]['queue'] == test_job_2['queue']
    assert response.json()[0]['owner'] == test_job_2['owner']
    assert response.json()[0]['path'] == test_job_2['path']
    assert response.json()[0]['options'] == test_job_2['options']

    response = client.get('/jobs', params={'owner': 'owner3'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_3['name']
    assert response.json()[0]['queue'] == test_job_3['queue']
    assert response.json()[0]['owner'] == test_job_3['owner']
    assert response.json()[0]['path'] == test_job_3['path']
    assert response.json()[0]['options'] == test_job_3['options']

    response = client.get('/jobs', params={'owner': 'owner4'})
    assert response.status_code == 200
    assert response.json() == []


def test_read_jobs_by_status(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get(
        '/jobs', params={'owner': 'root', 'status': JobStatus.TO_BE_QUEUED.value})
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[1]['name'] == test_job_2['name']
    assert response.json()[1]['queue'] == test_job_2['queue']
    assert response.json()[1]['owner'] == test_job_2['owner']
    assert response.json()[2]['name'] == test_job_3['name']
    assert response.json()[2]['queue'] == test_job_3['queue']
    assert response.json()[2]['owner'] == test_job_3['owner']

    response = client.get(
        '/jobs', params={'owner': 'root', 'status': JobStatus.RUNNING.value})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'root', 'status': 'WRONG_STATUS'})
    assert response.status_code == 422

    response = client.get(
        '/jobs', params={'owner': 'root', 'status': JobStatus.RUNNING.value})
    assert response.status_code == 200
    assert response.json() == []


def test_read_jobs_by_queue(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get('/jobs', params={'owner': 'root', 'queue': 1})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[1]['name'] == test_job_2['name']
    assert response.json()[1]['queue'] == test_job_2['queue']
    assert response.json()[1]['owner'] == test_job_2['owner']

    response = client.get('/jobs', params={'owner': 'root', 'queue': 2})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_3['name']
    assert response.json()[0]['queue'] == test_job_3['queue']
    assert response.json()[0]['owner'] == test_job_3['owner']

    response = client.get('/jobs', params={'owner': 'root', 'queue': 3})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'root', 'queue': 'WRONG_QUEUE'})
    assert response.status_code == 422


def test_read_jobs_by_owner_status(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get(
        '/jobs', params={'owner': 'owner1', 'status': JobStatus.TO_BE_QUEUED.value})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner2', 'status': JobStatus.TO_BE_QUEUED.value})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_2['name']
    assert response.json()[0]['queue'] == test_job_2['queue']
    assert response.json()[0]['owner'] == test_job_2['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner3', 'status': JobStatus.TO_BE_QUEUED.value})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_3['name']
    assert response.json()[0]['queue'] == test_job_3['queue']
    assert response.json()[0]['owner'] == test_job_3['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner4', 'status': JobStatus.TO_BE_QUEUED.value})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'owner1', 'status': JobStatus.RUNNING.value})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'owner2', 'status': JobStatus.RUNNING.value})
    assert response.status_code == 200
    assert response.json() == []


def test_read_jobs_by_owner_status_queue(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201
    response = client.post('/jobs', json=test_job_3)
    assert response.status_code == 201

    response = client.get(
        '/jobs', params={'owner': 'owner1', 'status': JobStatus.TO_BE_QUEUED.value, 'queue': 1})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner2', 'status': JobStatus.TO_BE_QUEUED.value, 'queue': 1})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_2['name']
    assert response.json()[0]['queue'] == test_job_2['queue']
    assert response.json()[0]['owner'] == test_job_2['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner3', 'status': JobStatus.TO_BE_QUEUED.value, 'queue': 2})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == test_job_3['name']
    assert response.json()[0]['queue'] == test_job_3['queue']
    assert response.json()[0]['owner'] == test_job_3['owner']

    response = client.get(
        '/jobs', params={'owner': 'owner4', 'status': JobStatus.TO_BE_QUEUED.value, 'queue': 1})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'owner1', 'status': JobStatus.RUNNING.value, 'queue': 1})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'owner2', 'status': JobStatus.RUNNING.value, 'queue': 1})
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(
        '/jobs', params={'owner': 'root', 'status': JobStatus.TO_BE_QUEUED.value, 'queue': 1})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['name'] == test_job_1['name']
    assert response.json()[0]['queue'] == test_job_1['queue']
    assert response.json()[0]['owner'] == test_job_1['owner']
    assert response.json()[1]['name'] == test_job_2['name']
    assert response.json()[1]['queue'] == test_job_2['queue']
    assert response.json()[1]['owner'] == test_job_2['owner']


def test_read_job(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_1['name']
    assert response.json()['queue'] == test_job_1['queue']
    assert response.json()['owner'] == test_job_1['owner']
    assert response.json()['path'] == test_job_1['path']
    assert response.json()['options'] == test_job_1['options']

    response = client.get('/jobs/1', params={'owner': 'owner2'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.get('/jobs/2', params={'owner': 'owner1'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.get('/jobs/2', params={'owner': 'owner2'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}


def test_read_job_no_options(client):
    response = client.post('/jobs', json=test_job_4_no_options)
    assert response.status_code == 201

    response = client.get('/jobs/1', params={'owner': 'owner4'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_4_no_options['name']
    assert response.json()['queue'] == test_job_4_no_options['queue']
    assert response.json()['owner'] == test_job_4_no_options['owner']
    assert response.json()['path'] == test_job_4_no_options['path']
    assert response.json()['options'] == ''


def test_update_job(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'name': 'job1_updated', 'queue': 2})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == 'job1_updated'
    assert response.json()['queue'] == 2
    assert response.json()['owner'] == 'owner1'

    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201

    response = client.put(
        '/jobs/2', params={'owner': 'owner2'}, json={'name': 'job2_updated', 'queue': 2})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/2', params={'owner': 'owner2'})
    assert response.status_code == 200
    assert response.json()['name'] == 'job2_updated'
    assert response.json()['queue'] == 2
    assert response.json()['owner'] == 'owner2'

    response = client.put(
        '/jobs/2', params={'owner': 'owner1'}, json={'name': 'job2_updated', 'queue': 2})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.put(
        '/jobs/2', params={'owner': 'owner2'}, json={'name': 'job2_updated_again', 'queue': 1})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/2', params={'owner': 'owner2'})
    assert response.status_code == 200
    assert response.json()['name'] == 'job2_updated_again'
    assert response.json()['queue'] == 1
    assert response.json()['owner'] == 'owner2'

    response = client.put(
        '/jobs/3', params={'owner': 'owner3'}, json={'name': 'job3_updated', 'queue': 1})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}


def test_update_job_name_only(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'name': 'job1_updated'})
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == 'job1_updated'
    assert response.json()['queue'] == test_job_1['queue']
    assert response.json()['owner'] == 'owner1'
    assert response.json()['status'] == JobStatus.TO_BE_QUEUED.value
    assert response.json()['path'] == test_job_1['path']
    assert response.json()['options'] == test_job_1['options']


def test_update_job_queue_only(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'queue': 2})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_1['name']
    assert response.json()['queue'] == 2
    assert response.json()['owner'] == 'owner1'
    assert response.json()['status'] == JobStatus.TO_BE_QUEUED.value
    assert response.json()['path'] == test_job_1['path']
    assert response.json()['options'] == test_job_1['options']


def test_update_job_status_only(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'status': JobStatus.RUNNING.value})
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_1['name']
    assert response.json()['queue'] == test_job_1['queue']
    assert response.json()['owner'] == 'owner1'
    assert response.json()['status'] == JobStatus.RUNNING.value
    assert response.json()['path'] == test_job_1['path']
    assert response.json()['options'] == test_job_1['options']


def test_update_job_path_only(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'path': '/path/to/job1_updated'})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_1['name']
    assert response.json()['queue'] == test_job_1['queue']
    assert response.json()['owner'] == 'owner1'
    assert response.json()['status'] == JobStatus.TO_BE_QUEUED.value
    assert response.json()['path'] == '/path/to/job1_updated'
    assert response.json()['options'] == test_job_1['options']


def test_update_job_options_only(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.put(
        '/jobs/1', params={'owner': 'owner1'}, json={'options': '--option1 value1_updated --option2 value2_updated'})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job updated successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json()['name'] == test_job_1['name']
    assert response.json()['queue'] == test_job_1['queue']
    assert response.json()['owner'] == 'owner1'
    assert response.json()['status'] == JobStatus.TO_BE_QUEUED.value
    assert response.json()['path'] == test_job_1['path']
    assert response.json()[
        'options'] == '--option1 value1_updated --option2 value2_updated'


def test_delete_job(client):
    response = client.post('/jobs', json=test_job_1)
    assert response.status_code == 201

    response = client.delete('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job deleted successfully ✅'}

    response = client.get('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/1', params={'owner': 'owner1'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.post('/jobs', json=test_job_2)
    assert response.status_code == 201

    response = client.delete('/jobs/2', params={'owner': 'owner2'})
    assert response.status_code == 200
    assert response.json() == {'status': 'success',
                               'message': 'Job deleted successfully ✅'}

    response = client.get('/jobs/2', params={'owner': 'owner2'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/3', params={'owner': 'owner3'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/1', params={'owner': 'owner2'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/2', params={'owner': 'owner1'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/3', params={'owner': 'owner4'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}

    response = client.delete('/jobs/4', params={'owner': 'owner3'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Job not found'}
