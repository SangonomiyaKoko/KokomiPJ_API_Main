
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from .scripts.api_users import API_Users
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
    result = await API_Users.get_api_user()
    return result

@router.post('/api-users')
async def add_api_user(user: ApiUser):
    result = await API_Users.add_api_user(
        username=user.username,
        password=user.password,
        roles=user.roles
    )
    return result

@router.delete('/api-users/{username}')
async def delete_api_user(username: str):
    result = await API_Users.del_api_user(
        username=username
    )
    return result