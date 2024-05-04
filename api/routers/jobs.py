from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.utils.database_helper import DatabaseHelper

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


class PostJobModel(BaseModel):
    name: str
    queue: int
    owner: str


class PutJobModel(BaseModel):
    name: str
    queue: int


@router.get("")
def read_jobs(owner: str, status: JobStatus = None, queue: int = None):
    return DatabaseHelper().get_jobs(owner=owner, status=status, queue=queue)


@router.get("/{job_id}")
def read_job(job_id: int, owner: str):
    try:
        return DatabaseHelper().get_job(job_id, owner)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", status_code=201)
def create_job(job: PostJobModel):
    try:
        DatabaseHelper().insert_job(Job(name=job.name, queue=job.queue, owner=job.owner))
        return {"status": "success", "message": "Job created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{job_id}")
def update_job(job_id: int, owner: str, job: PutJobModel):
    stored_job = read_job(job_id, owner)
    if stored_job.status != JobStatus.QUEUED.value:
        raise HTTPException(
            status_code=400, detail="Only QUEUED jobs can be updated")
    try:
        DatabaseHelper().update_job(job_id, owner, Job(name=job.name, queue=job.queue))
        return {"status": "success", "message": "Job updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}")
def delete_job(job_id: int, owner: str):
    stored_job = read_job(job_id, owner)
    if stored_job.status != JobStatus.QUEUED.value:
        raise HTTPException(
            status_code=400, detail="Only QUEUED jobs can be deleted")
    try:
        DatabaseHelper().delete_job(job_id, owner)
        return {"status": "success", "message": "Job deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
