# -*- coding: utf-8 -*-

import traceback
import time
from typing import TypedDict
from ..model.users import User, User_Basic_DB
from ..model.clans import Clan, Clan_Basic_DB
from ..net.basic import get_basic_data, get_basic_and_clan_data
from .. import CLAN_BLACKLIST, USER_BLACKLIST, GAME_CONST
from .. import settings
from .. import SuccessResponse, InfoResponse, ErrorResponse

class user_info(TypedDict):
    aid: str
    nickname: str
    server: str
    battles: int
    karma: int
    registration_date: str
    last_battle_time: str

class clan_info(TypedDict):
    cid: str
    tag: str
    color: int

async def main(
    aid: str,
    region: str,
    lang: str,
    opt_pr: bool = True,
    opt_ac: bool = True,
    ac: str = None
) -> dict:
    try:
        params = []
        result = {}
        user_basic_db = User_Basic_DB()
        clan_basic_db = Clan_Basic_DB()
        if aid in USER_BLACKLIST:
            result = InfoResponse(message='USER IN BLACKLIST')
            return result
        user_result: SuccessResponse | ErrorResponse = user_basic_db.get_user_data(
            account_id=aid,
            server=region
        )
        if user_result.status != 'ok':
            return user_result
        user_basic_data: User = user_result.data
        current_time = int(time.time())
        clan_cache_vaild = False
        cid = None
        clan_tag = None
        clan_color = None
        if (
            current_time - user_basic_data['clan_update_time'] < 
            settings.CLAN_CACHE_VALIDITY*24*60*60
        ):
            clan_id = user_basic_data['clan_id']
            if clan_id:
                clan_result: SuccessResponse | ErrorResponse = clan_basic_db.get_clan_data(
                    clan_id = clan_id,
                    region = region
                )
                if clan_result.status != 'ok':
                    return clan_result
                clan_basic_data: Clan = clan_result.data
                if (
                    current_time - clan_basic_data['update_time'] <
                    settings.CLAN_CACHE_VALIDITY_2*24*60*60
                ):
                    clan_cache_vaild = True
                    cid = clan_id
                    clan_tag = clan_basic_data['clan_tag']
                    clan_color = clan_basic_data['clan_color']
        if clan_cache_vaild:
            call_api_data = await get_basic_and_clan_data(
                aid=aid,
                server=region,
                use_ac=opt_ac,
                ac=ac
            )
            for response in call_api_data:
                if type(response) != SuccessResponse:
                    return response
            user_data: dict = call_api_data[0].data
            clan_data: dict = call_api_data[1].data
            if clan_data['data'].get('clan_id', None) != None:
                cid = clan_data['data']['clan_id']
                clan_tag = clan_data['data']['clan']['tag']
                clan_color = GAME_CONST.CLAN_COLOR_INDEX.get(clan_data['data']['clan']['color'],4)
                clan_basic_db.update_clan_info(
                    clan_id=cid,
                    region=region,
                    clan_tag=clan_tag,
                    clan_color=clan_color,
                    update_time=current_time
                )
            user_basic_db.update_user_clan(
                account_id=aid,
                region=region,
                clan_id=cid,
                clan_update_time=current_time
            )
        else:
            call_api_data = await get_basic_data(
                aid=aid,
                server=region,
                use_ac=opt_ac,
                ac=ac
            )
            for response in call_api_data:
                if type(response) != SuccessResponse:
                    return response
            user_data = call_api_data[0].data



        
        
    except Exception:
        traceback.print_exc()
        ...
    finally:
        ...