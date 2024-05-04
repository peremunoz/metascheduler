from fastapi import APIRouter, HTTPException

from api.config.config import AppConfig


router = APIRouter(
    prefix='/nodes',
    tags=['Nodes'],
    responses={404: {'description': 'Not found'}},
)


@router.get('')
async def read_nodes():
    return [{'id': node.id_, 'ip': node.ip, 'port': node.port, 'is_alive': node.is_alive}
            for node in AppConfig().nodes]


@router.get('/master')
async def read_master_node():
    master_node = AppConfig().master_node
    return {
        'id': master_node.id_,
        'ip': master_node.ip,
        'port': master_node.port,
        'is_alive': master_node.is_alive
    }


@router.get('/{node_id}')
async def read_node(node_id: int):
    if node_id >= len(AppConfig().nodes):
        raise HTTPException(status_code=404, detail='Node not found')
    node = AppConfig().nodes[node_id]

    return {
        'id': node.id_,
        'ip': node.ip,
        'port': node.port,
        'is_alive': node.is_alive
    }
