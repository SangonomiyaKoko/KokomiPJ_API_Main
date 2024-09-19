
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from .scripts import (
    api_add_user,
    api_del_user,
    api_get_user
)
router = APIRouter()    

class ApiUser(BaseModel):
    username: str
    password: str
    roles: str

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


@router.get('/api-users')
async def get_api_users():
    return await api_get_user.main()

@router.post('/api-users')
async def add_api_user(user: ApiUser):
    return await api_add_user.main(
        username=user.username,
        password=user.password,
        roles=user.roles
    )

@router.delete('/api-users/{username}')
async def delete_api_user(username: str):
    return await api_del_user.main(
        username=username
    )