from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.utils.database_helper import DatabaseHelper

router = APIRouter(
    prefix='/jobs',
    tags=['Jobs'],
)


class PostJobModel(BaseModel):
    name: str
    queue: int
    owner: str
    path: str
    options: str = ''


class PutJobModel(BaseModel):
    name: str = None
    queue: int = None
    status: JobStatus = None
    path: str = None
    options: str = None


@router.get('')
def read_jobs(owner: str, status: JobStatus = None, queue: int = None):
    return DatabaseHelper().get_jobs(owner=owner, status=status, queue=queue)


@router.get('/{job_id}')
def read_job(job_id: int, owner: str):
    try:
        return DatabaseHelper().get_job(job_id, owner)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post('', status_code=201)
def create_job(job: PostJobModel):
    try:
        DatabaseHelper().insert_job(Job(name=job.name, queue=job.queue,
                                        owner=job.owner, path=job.path, options=job.options))
        return {'status': 'success', 'message': 'Job created successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put('/{job_id}')
def update_job(job_id: int, owner: str, job: PutJobModel):
    stored_job = read_job(job_id, owner)
    if stored_job.status.value is not JobStatus.QUEUED.value:
        raise HTTPException(
            status_code=400, detail='Only QUEUED jobs can be updated')
    try:
        DatabaseHelper().update_job(job_id, owner, Job(name=job.name or stored_job.name, queue=job.queue or stored_job.queue,
                                                       status=job.status or stored_job.status, path=job.path or stored_job.path,
                                                       options=job.options or stored_job.options))
        return {'status': 'success', 'message': 'Job updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def update_job_status(job_id: int, owner: str, status: JobStatus):
    ''' Update the status of a job '''
    stored_job = read_job(job_id, owner)
    if stored_job.status.value is status.value:
        return {'status': 'success', 'message': 'Job status not changed'}
    try:
        DatabaseHelper().update_job(job_id, owner, Job(name=stored_job.name, queue=stored_job.queue,
                                                       status=status, path=stored_job.path,
                                                       options=stored_job.options))
        return {'status': 'success', 'message': 'Job updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def set_job_scheduler_job_id(job_id: int, owner: str, scheduler_job_id: int):
    ''' Set the scheduler job ID of a job '''
    read_job(job_id, owner)
    try:
        DatabaseHelper().set_job_scheduler_id(job_id, owner, scheduler_job_id)
        return {'status': 'success', 'message': 'Job updated successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete('/{job_id}')
def delete_job(job_id: int, owner: str):
    stored_job = read_job(job_id, owner)
    if stored_job.status.value is not JobStatus.QUEUED.value:
        raise HTTPException(
            status_code=400, detail='Only QUEUED jobs can be deleted')
    try:
        DatabaseHelper().delete_job(job_id, owner)
        return {'status': 'success', 'message': 'Job deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
