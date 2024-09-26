# -*- coding: utf-8 -*-

import traceback
import time
import gc
from typing import TypedDict
from ..model.users import User, User_Basic_DB, User_Info_DB
from ..model.clans import Clan, Clan_Basic_DB
from ..net.basic import get_basic_data, get_basic_and_clan_data
from .. import CLAN_BLACKLIST, USER_BLACKLIST, GAME_CONST
from .. import settings
from .. import API_Logging
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

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
    verson: str,
    opt_pr: bool = True,
    opt_ac: bool = True,
    ac: str = None
) -> dict:
    try:
        params = []
        result = None
        if aid in USER_BLACKLIST:
            result = InfoResponse(message='USER IN BLACKLIST')
            return result
        if verson not in settings.VERSON_LIST:
            result = InfoResponse(message='VERSON ERROR')
            return result
        user_basic_db = User_Basic_DB()
        user_info_db = User_Info_DB()
        clan_basic_db = Clan_Basic_DB()
        user_result: SuccessResponse | ErrorResponse = await user_basic_db.get_user_data(
            account_id=aid,
            region=region
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
                clan_result: SuccessResponse | ErrorResponse = await clan_basic_db.get_clan_data(
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
        if not clan_cache_vaild:
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
            if clan_data.get('clan_id', None) != None:
                cid = clan_data['clan_id']
                clan_tag = clan_data['clan']['tag']
                clan_color = GAME_CONST.CLAN_COLOR_INDEX.get(clan_data['clan']['color'],4)
                await clan_basic_db.update_clan_info(
                    clan_id=cid,
                    region=region,
                    clan_tag=clan_tag,
                    clan_color=clan_color,
                    update_time=current_time
                )
            await user_basic_db.update_user_clan(
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
        if cid in CLAN_BLACKLIST:
            result = InfoResponse(message='CLAN IN BLACKLIST')
            return result
        user_hidden = False
        user_lp = 0
        user_lbt = 0
        nickname = user_data[aid]['name']
        if nickname != user_basic_data['nickname']:
            await user_basic_db.update_user_name(
                account_id=aid,
                region=region,
                nickname=nickname
            )
        if 'hidden_profile' in user_data[aid]:
            user_hidden = True
        if (
            user_data[aid]['statistics'] == {} or 
            user_data[aid]['statistics']['basic'] == {}
        ):
            pass
        else:
            basic_data: dict = user_data[aid]['statistics']['basic']
            user_lp = basic_data.get('leveling_points', 0)
            user_lbt = basic_data.get('last_battle_time',0)
        await user_info_db.check_user_data(
            account_id=aid,
            region=region,
            update_time=current_time,
            profite=user_hidden,
            leveling_points=user_lp,
            last_battle_time=user_lbt
        )

        # main 
        result = SuccessResponse(data={})

        await user_basic_db.update_user_query(
            account_id=aid,
            region=region
        )
        return result
    except Exception as e:
        error_info = traceback.format_exc()
        track_id = API_Logging().write_api_error(
            error_file=__file__,
            error_params=params,
            error_name=str(type(e).__name__),
            error_info=error_info
        )
        error = BaseError(
            error_info=str(type(e).__name__),
            track_id=track_id
        )
        result = ErrorResponse(
            message='PROGRAM ERROR',
            data=error
        )
        return result
    finally:
        gc.collect()