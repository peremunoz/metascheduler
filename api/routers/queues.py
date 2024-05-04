from fastapi import APIRouter

from api.utils.database_helper import DatabaseHelper


router = APIRouter(
    prefix='/queues',
    tags=['Queues'],
)


@router.get('')
def read_queues():
    queues = DatabaseHelper().get_queues()
    return [{'id': queue.id_, 'scheduler_name': queue.scheduler_name} for queue in queues]
