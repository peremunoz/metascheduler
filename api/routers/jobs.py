from fastapi import APIRouter
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
    job_obj = Job(job.name, get_scheduler(job.scheduler))
    DatabaseHelper().insert_job(job_obj)
    return {"job": job_obj}
