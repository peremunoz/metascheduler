from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.constants.cluster_mode import ClusterMode
from api.routers import nodes
from api.config.config import AppConfig


router = APIRouter(
    prefix='/cluster',
    tags=['Cluster'],
)

router.include_router(nodes.router)


class PutClusterModeModel(BaseModel):
    user: str
    mode: ClusterMode


@router.get('/mode')
def read_cluster_mode():
    return AppConfig().get_mode()


@router.put('/mode')
def update_cluster_mode(data: PutClusterModeModel):
    if data.user == 'root':
        AppConfig().set_mode(data.mode)
        return {'message': 'Cluster mode updated successfully ✅'}
    raise HTTPException(status_code=403, detail='Forbidden')
