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


@router.get("")
def read_jobs():
    return DatabaseHelper().get_jobs()


@router.post("")
def create_job(job: JobModel):
    try:
        job_obj = Job(job.name, get_scheduler(job.scheduler))
        DatabaseHelper().insert_job(job_obj)
        return {"job": job_obj}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
