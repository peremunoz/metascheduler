from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.interfaces.Job import Job
from api.utils.DatabaseHelper import DatabaseHelper

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


class JobModel(BaseModel):
    name: str
    scheduler: str
    owner: str


@router.get("")
def read_jobs():
    return DatabaseHelper().get_jobs()


@router.post("", status_code=201)
def create_job(job: JobModel):
    try:
        queue_id = DatabaseHelper().get_queue_id(job.scheduler)
        DatabaseHelper().insert_job(Job(name=job.name, queue=queue_id, owner=job.owner))
        return {"status": "success", "message": "Job created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
