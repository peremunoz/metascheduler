from fastapi import APIRouter

from api.utils.database_helper import DatabaseHelper


router = APIRouter(
    prefix='/queues',
    tags=['Queues'],
)


@router.get('')
def read_queues():
    return DatabaseHelper().get_queues()
