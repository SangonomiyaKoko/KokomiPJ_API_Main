
from fastapi import APIRouter
from .scripts import (
    api_add_user,
    api_del_user,
    api_get_user
)
router = APIRouter()

@router.get("/status")
async def getApiStatus(
    params: str
):
    """
    Get server status.

    - **params**: The data parameters to be queried

    - **Return**: JSON object:

    For more returned data, please refer to the detailed interface documentation: [DocsLink](https://example.com/items-docs)
    """
    return {
        'status': 'ok',
        'message': 'SUCCESS',
        'data': {
            'params': params
        }
    }

@router.get('/get-api-user')
async def getApiUser():
    return await api_get_user.main()

@router.post('/add-api-user')
async def addApiUser(
    username: str,
    password: str,
    roles: str
):
    return await api_add_user.main(
        username=username,
        password=password,
        roles=roles
    )

@router.delete('/del-api-user')
async def delApiUser(
    username: str
):
    return await api_del_user.main(
        username=username
    )