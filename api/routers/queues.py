from fastapi import APIRouter, HTTPException

from api.utils.database_helper import DatabaseHelper


router = APIRouter(
    prefix="/queues",
    tags=["Queues"],
)


@router.get("")
def read_queues():
    return DatabaseHelper().get_queues()
