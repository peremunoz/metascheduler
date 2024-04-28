from fastapi import APIRouter, HTTPException

from config.config import AppConfig


router = APIRouter(
    prefix="/nodes",
    tags=["Nodes"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def read_nodes():
    return [{"id": node.id, "ip": node.ip, "port": node.port, "ssh_user": node.ssh_user, "is_alive": node.is_alive()} for node in AppConfig().nodes]


@router.get("/master")
async def read_master_node():
    return AppConfig().master_node


@router.get("/{node_id}")
async def read_node(node_id: int):
    if node_id >= len(AppConfig().nodes):
        raise HTTPException(status_code=404, detail="Node not found")

    node = AppConfig().nodes[node_id]

    return {
        "id": node.id,
        "ip": node.ip,
        "port": node.port,
        "ssh_user": node.ssh_user,
        "is_alive": node.is_alive()
    }
