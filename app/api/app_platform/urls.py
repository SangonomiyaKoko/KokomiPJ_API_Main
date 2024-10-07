
from fastapi import APIRouter, BackgroundTasks

from .. import API_Tracker


router = APIRouter()    


@router.get('/user-stats')
async def get_api_users(
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(func=API_Tracker().record_api_call)
