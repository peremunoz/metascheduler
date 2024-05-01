from fastapi import APIRouter
from api.routers import nodes
from api.config.config import AppConfig


router = APIRouter(
    prefix="/cluster",
    tags=["Cluster"],
)

router.include_router(nodes.router)


@router.get("/mode")
def read_cluster_mode():
    return AppConfig().mode.value
