
from fastapi import APIRouter

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
    return {
        'status': 'ok',
        'message': 'SUCCESS',
        'data': {}
    }

@router.post('/add-api-user')
async def addApiUser():
    return {
        'status': 'ok',
        'message': 'SUCCESS',
        'data': {}
    }

@router.delete('/del-api-user')
async def delApiUser():
    return {
        'status': 'ok',
        'message': 'SUCCESS',
        'data': {}
    }