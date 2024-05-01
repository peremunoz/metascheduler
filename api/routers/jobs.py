from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from interfaces.Job import Job
from utils.DatabaseHelper import DatabaseHelper
from utils.SchedulerFactory import get_scheduler

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
        DatabaseHelper().insert_job(Job(job.name, get_scheduler(job.scheduler), job.owner))
        return {"status": "success", "message": "Job created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
