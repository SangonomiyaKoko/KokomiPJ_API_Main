
from fastapi import APIRouter, BackgroundTasks
from enum import Enum
from .scripts import (
    status
)
from . import API_Tracker


class ServerName(str, Enum):
    asia = "asia"
    eu = "eu"
    na = "na"
    ru = "ru"
    cn = "cn"
    
class Lang(str, Enum):
    cn = 'cn'
    en = 'en'
    ja = 'ja'

class Verson(str, Enum):
    v_1_0_1 = 'v_1_0_1'


router = APIRouter()    


@router.get('/user-stats')
async def get_api_users(
    background_tasks: BackgroundTasks,
    aid: str = '2023619512',
    region: ServerName = 'asia',
    lang: Lang = 'en',
    verson: Verson = 'v_1_0_1',
    opt_pr: bool = True,
    opt_ac: bool = False,
    ac: str = None
):
    result = await status.main(
        aid=aid,
        region=region,
        lang=lang,
        verson=verson,
        opt_pr=opt_pr,
        opt_ac=opt_ac,
        ac=ac
    )
    background_tasks.add_task(func=API_Tracker().record_api_call)
    return result.to_dict()
