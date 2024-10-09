# -*- coding: utf-8 -*-

import traceback
import time
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
    params = []
    result = None
    try:
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


    
# def other_data_processing(
#     aid: str,
#     server: str,
#     lang: str,
#     responses: dict,
#     result: dict
# ):
#     res_data = {}
#     i = 0
#     for response in responses:
#         type_index_list = ['pvp','pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']
#         for ship_id, ship_data in response['data'][aid]['statistics'].items():
#             if ship_id not in res_data:
#                 res_data[ship_id] = {
#                     'pvp':{},
#                     'pvp_solo':{},
#                     'pvp_div2':{},
#                     'pvp_div3':{},
#                     'rank_solo':{}
#                 }
#             battle_type=type_index_list[i]
#             res_data[ship_id][battle_type] = {
#                 'battles_count': 0,
#                 'wins': 0,
#                 'damage_dealt': 0,
#                 'frags': 0,
#                 'original_exp': 0,
#                 'survived': 0,
#                 'hits_by_main': 0,
#                 'shots_by_main': 0,
#                 'value_battles_count': 0,
#                 'personal_rating': 0,
#                 'n_damage_dealt': 0,
#                 'n_frags': 0
#             }
#             if ship_data[battle_type] != {}:
#                 for index in ['battles_count','wins','damage_dealt','frags','original_exp','survived','hits_by_main','shots_by_main']:
#                     res_data[ship_id][battle_type][index] = ship_data[battle_type][index]
#         i += 1
#     ship_id_list = list(res_data.keys())
#     ship_data_dict = Ship_Data.get_ship_data_dict(ship_id_list,server)
#     ship_info_dict = Ship_Name.get_ship_info_dict(ship_id_list,lang,server)

#     json_data = responses[0]['data'][aid]['statistics']
#     if json_data == {}:
#         pass
#     else:
#         index_list = [
#             'max_planes_killed',
#             'max_damage_dealt',
#             'max_exp',
#             'max_frags',
#             'max_total_agro',
#             'max_scouting_damage'
#         ]
#         for index in index_list:
#             result['data']['stats']['record'][index] = {
#                 'ship_data': 0,
#                 'ship_info': {
#                     "tier": 1,
#                     "type": "Cruiser",
#                     "nation": "germany",
#                     "ship_name": "Unknow"
#                 }
#             }
#         for ship_id, ship_data in json_data.items():
#             if ship_data == {} or ship_data['pvp'] == {}:
#                 continue
#             if ship_info_dict.get(ship_id,None) == None:
#                 continue
#             for index in index_list:
#                 if ship_data['pvp'][index] > result['data']['stats']['record'][index]['ship_data']:
#                     ship_name_data = ship_info_dict.get(ship_id,None)
#                     result['data']['stats']['record'][index] = {
#                         'ship_data': ship_data['pvp'][index],
#                         'ship_info': {
#                             "tier": ship_name_data['ship_tier'],
#                             "type": ship_name_data['ship_type'],
#                             "nation": ship_name_data['ship_nation'],
#                             "ship_name": ship_name_data['ship_name']
#                         }
#                     }
    
#     result_data = {}
#     for ship_id, ship_data in res_data.items():
#         result_data[ship_id] = Personal_Rating.get_personal_rating_2(
#             ship_id=ship_id,
#             ship_dict=ship_data,
#             server_data=ship_data_dict.get(ship_id, None)
#         )
#     result['data']['stats']['overview'] = {
#         'pvp': {},
#         'pvp_solo': {},
#         'pvp_div2': {},
#         'pvp_div3': {},
#         'rank': {}
#     }
#     result['data']['stats']['ship_type'] = {
#         'AirCarrier': {},
#         'Battleship': {},
#         'Cruiser': {},
#         'Destroyer': {},
#         'Submarine': {}
#     }
#     result['data']['stats']['ship_tier'] = {
#         1: 0, 
#         2: 0, 
#         3: 0, 
#         4: 0, 
#         5: 0, 
#         6: 0, 
#         7: 0, 
#         8: 0, 
#         9: 0, 
#         10: 0, 
#         11: 0
#     }
#     for index in ['pvp','pvp_solo','pvp_div2','pvp_div3','rank']:
#         result['data']['stats']['overview'][index] = {
#             'battles_count': 0,
#             'wins': 0,
#             'damage_dealt': 0,
#             'frags': 0,
#             'original_exp': 0,
#             'survived': 0,
#             'hits_by_main': 0,
#             'shots_by_main': 0,
#             'value_battles_count': 0,
#             'personal_rating': 0,
#             'n_damage_dealt': 0,
#             'n_frags': 0
#         }
#     for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
#         result['data']['stats']['ship_type'][index] = {
#             'battles_count': 0,
#             'wins': 0,
#             'damage_dealt': 0,
#             'frags': 0,
#             'original_exp': 0,
#             'value_battles_count': 0,
#             'personal_rating': 0,
#             'n_damage_dealt': 0,
#             'n_frags': 0
#         }
#     for ship_id, ship_data in result_data.items():
#         ship_info_data = ship_info_dict.get(ship_id,None)
#         if ship_info_data is None:
#             continue
#         ship_tier = ship_info_data['ship_tier']
#         ship_type = ship_info_data['ship_type']
#         for battle_type in ['pvp','pvp_solo','pvp_div2','pvp_div3']:
#             for index in ['battles_count','wins','damage_dealt','frags','original_exp','survived','hits_by_main','shots_by_main']:
#                 result['data']['stats']['overview'][battle_type][index] += ship_data[battle_type][index]
#                 if battle_type == 'pvp':
#                     if index not in ['survived','hits_by_main','shots_by_main']:
#                         result['data']['stats']['ship_type'][ship_type][index] += ship_data[battle_type][index]
#                     if index == 'battles_count':
#                         result['data']['stats']['ship_tier'][ship_tier] += ship_data[battle_type][index]

#             if ship_data[battle_type]['value_battles_count'] > 0:
#                 for index in ['value_battles_count','personal_rating','n_damage_dealt','n_frags']:
#                     result['data']['stats']['overview'][battle_type][index] += ship_data[battle_type][index]
#                     if battle_type == 'pvp':
#                         result['data']['stats']['ship_type'][ship_type][index] += ship_data[battle_type][index]
#         for battle_type in ['rank_solo']:
#             for index in ['battles_count','wins','damage_dealt','frags','original_exp','survived','hits_by_main','shots_by_main']:
#                 result['data']['stats']['overview']['rank'][index] += ship_data[battle_type][index]
#             if ship_data[battle_type]['value_battles_count'] > 0:
#                 for index in ['value_battles_count','personal_rating','n_damage_dealt','n_frags']:
#                     result['data']['stats']['overview']['rank'][index] += ship_data[battle_type][index]
#     return result


# def finish_data_processing(
#     use_pr: bool,
#     lang: str,
#     result: dict,
# ):
#     temp_dict = {
#         'pvp': {},
#         'pvp_solo': {},
#         'pvp_div2': {},
#         'pvp_div3': {},
#         'rank': {}
#     }
#     index_list = ['pvp','pvp_solo','pvp_div2','pvp_div3','rank']
#     for index in index_list:
#         pro_data = {
#             'battles_count': 0,
#             'win_rate': '0%',
#             'win_rate_progress': 2,
#             'pr_score': 0,
#             'pr_score_progress': 2,
#             'pr_rate': 'Unkown',
#             'pr_text': 'Next Level: +1',
#             'avg_damage': 0,
#             'avg_frags': 0.0,
#             'avg_exp': 0,
#             'k_d': 0.0,
#             'survial_rate': '0%',
#             'hit_ratio': '0%',
#             'win_rate_color': '#ffffff',
#             'avg_damage_color': '#ffffff',
#             'avg_frags_color': '#ffffff',
#             'pr_color': '#808080'
#         }
#         if result['data']['stats']['overview'][index]['battles_count'] != 0:
#             pro_data['battles_count'] = result['data']['stats']['overview'][index]['battles_count']
#             pro_data['win_rate'] = round(result['data']['stats']['overview'][index]['wins']/result['data']['stats']['overview'][index]['battles_count']*100,1)
#             if pro_data['win_rate'] <= 25:
#                 pro_data['win_rate_progress'] = 2
#             elif pro_data['win_rate'] >= 75:
#                 pro_data['win_rate_progress'] = 100
#             else:
#                 pro_data['win_rate_progress'] = int((98/50)*(pro_data['win_rate']-25))+2
#             pro_data['avg_damage'] = int(result['data']['stats']['overview'][index]['damage_dealt']/result['data']['stats']['overview'][index]['battles_count'])
#             pro_data['avg_frags'] = round(result['data']['stats']['overview'][index]['frags']/result['data']['stats']['overview'][index]['battles_count'],2)
#             pro_data['avg_exp'] = int(result['data']['stats']['overview'][index]['original_exp']/result['data']['stats']['overview'][index]['battles_count'])
#             if result['data']['stats']['overview'][index]['battles_count']-result['data']['stats']['overview'][index]['survived'] == 0:
#                 pro_data['k_d'] = 999
#             else:
#                 pro_data['k_d'] = round(result['data']['stats']['overview'][index]['frags']/(result['data']['stats']['overview'][index]['battles_count']-result['data']['stats']['overview'][index]['survived']),2)
#             pro_data['survial_rate'] = str(round(result['data']['stats']['overview'][index]['survived']/result['data']['stats']['overview'][index]['battles_count']*100,1)) + '%'
#             if result['data']['stats']['overview'][index]['shots_by_main'] == 0:
#                 pro_data['hit_ratio'] = '0%'
#             else:
#                 pro_data['hit_ratio'] = str(round(result['data']['stats']['overview'][index]['hits_by_main']/result['data']['stats']['overview'][index]['shots_by_main']*100,1))+'%'
#             if use_pr is False:
#                 pro_data['pr_score'] = 0
#             elif result['data']['stats']['overview'][index]['value_battles_count'] == 0:
#                 pro_data['pr_score'] = 0
#             else:
#                 pro_data['pr_score'] = int(result['data']['stats']['overview'][index]['personal_rating']/result['data']['stats']['overview'][index]['value_battles_count'])
#             if pro_data['pr_score'] >= 2450:
#                 pro_data['pr_score_progress'] = 100
#             else:
#                 pro_data['pr_score_progress'] = max(int((98/2450)*pro_data['pr_score']),2)
#             pr_data = Personal_Rating.get_app_pr_info(pro_data['pr_score'],lang)
#             pro_data['pr_color'] = pr_data[0]
#             pro_data['pr_text'] = pr_data[1]
#             pro_data['pr_rate'] = pr_data[2]
#             if pro_data['pr_score'] != 0:
#                 pro_data['win_rate_color'] = Personal_Rating.get_app_color(0,pro_data['win_rate'])
#                 if result['data']['stats']['overview'][index]['value_battles_count'] != 0:
#                     pro_data['avg_damage_color'] = Personal_Rating.get_app_color(1,result['data']['stats']['overview'][index]['n_damage_dealt']/result['data']['stats']['overview'][index]['value_battles_count'])
#                 else:
#                     pro_data['avg_damage_color'] = Personal_Rating.get_app_color(1,-1)
#                 if result['data']['stats']['overview'][index]['value_battles_count'] != 0:
#                     pro_data['avg_frags_color'] = Personal_Rating.get_app_color(2,result['data']['stats']['overview'][index]['n_frags']/result['data']['stats']['overview'][index]['value_battles_count'])
#                 else:
#                     pro_data['avg_frags_color'] = Personal_Rating.get_app_color(2,-1)
#             pro_data['win_rate'] = str(pro_data['win_rate']) + '%'
#         temp_dict[index] = pro_data
#     result['data']['stats']['overview'] = {}
#     result['data']['stats']['overview'] = temp_dict

#     temp_dict = {
#         'AirCarrier': {},
#         'Battleship': {},
#         'Cruiser': {},
#         'Destroyer': {},
#         'Submarine': {},
#         'charts_list': []
#     }
#     charts_list = []
#     index_list = ['AirCarrier','Battleship','Cruiser','Destroyer','Submarine']
#     for index in index_list:
#         pro_data = {
#             'battles_count': 0,
#             'win_rate': '0%',
#             'pr_score': 0,
#             'avg_damage': 0,
#             'avg_frags': 0.0,
#             'avg_exp': 0,
#             'win_rate_color': '#ffffff',
#             'avg_damage_color': '#ffffff',
#             'avg_frags_color': '#ffffff',
#             'pr_color': '#808080'
#         }
#         if result['data']['stats']['ship_type'][index] == {} or result['data']['stats']['ship_type'][index]['battles_count'] == 0:
#             charts_list.append(0)
#             pass
#         else:
#             charts_list.append(result['data']['stats']['ship_type'][index]['battles_count'])
#             pro_data['battles_count'] = result['data']['stats']['ship_type'][index]['battles_count']
#             pro_data['win_rate'] = round(result['data']['stats']['ship_type'][index]['wins']/result['data']['stats']['ship_type'][index]['battles_count']*100,2)
#             pro_data['avg_damage'] = int(result['data']['stats']['ship_type'][index]['damage_dealt']/result['data']['stats']['ship_type'][index]['battles_count'])
#             pro_data['avg_frags'] = round(result['data']['stats']['ship_type'][index]['frags']/result['data']['stats']['ship_type'][index]['battles_count'],2)
#             pro_data['avg_exp'] = int(result['data']['stats']['ship_type'][index]['original_exp']/result['data']['stats']['ship_type'][index]['battles_count'])
#             if use_pr is False:
#                 pro_data['pr_score'] = 0
#             elif result['data']['stats']['ship_type'][index]['value_battles_count'] == 0:
#                 pro_data['pr_score'] = 0
#             else:
#                 pro_data['pr_score'] = int(result['data']['stats']['ship_type'][index]['personal_rating']/result['data']['stats']['ship_type'][index]['value_battles_count'])
#             pr_data = Personal_Rating.get_app_pr_info(pro_data['pr_score'],lang)
#             pro_data['pr_color'] = pr_data[0]
#             if pro_data['pr_score'] != 0:
#                 pro_data['win_rate_color'] = Personal_Rating.get_app_color(0,pro_data['win_rate'])
#                 if result['data']['stats']['ship_type'][index]['value_battles_count'] != 0:
#                     pro_data['avg_damage_color'] = Personal_Rating.get_app_color(1,result['data']['stats']['ship_type'][index]['n_damage_dealt']/result['data']['stats']['ship_type'][index]['value_battles_count'])
#                 else:
#                     pro_data['avg_damage_color'] = Personal_Rating.get_app_color(1,-1)
#                 if result['data']['stats']['ship_type'][index]['value_battles_count'] != 0:
#                     pro_data['avg_frags_color'] = Personal_Rating.get_app_color(2,result['data']['stats']['ship_type'][index]['n_frags']/result['data']['stats']['ship_type'][index]['value_battles_count'])
#                 else:
#                     pro_data['avg_frags_color'] = Personal_Rating.get_app_color(2,-1)
#             pro_data['win_rate'] = str(pro_data['win_rate']) + '%'
#         temp_dict[index] = pro_data
#     temp_dict['charts_list'] = charts_list
#     result['data']['stats']['ship_type'] = {}
#     result['data']['stats']['ship_type'] = temp_dict
#     charts_list = []
#     for tier in [1,2,3,4,5,6,7,8,9,10,11]:
#         charts_list.append(result['data']['stats']['ship_tier'][tier])
#     result['data']['stats']['ship_tier'] = []
#     result['data']['stats']['ship_tier'] = charts_list
#     return result