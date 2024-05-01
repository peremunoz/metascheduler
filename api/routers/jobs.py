from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.interfaces.Job import Job
from api.utils.DatabaseHelper import DatabaseHelper

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


class PostJobModel(BaseModel):
    name: str
    queue: int
    owner: str


@router.get("")
def read_jobs(owner: str):
    if owner == 'root':
        return DatabaseHelper().get_jobs()
    return DatabaseHelper().get_jobs(owner)


@router.post("", status_code=201)
def create_job(job: PostJobModel):
    try:
        DatabaseHelper().insert_job(Job(name=job.name, queue=job.queue, owner=job.owner))
        return {"status": "success", "message": "Job created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
