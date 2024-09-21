# import httpx
# import time
# from httpx import TimeoutException, ConnectTimeout, ReadTimeout
# import asyncio
# import traceback
# import gc


# async def fetch_data(url):
#     async with httpx.AsyncClient() as client:
#         try:
#             res = await client.get(url, timeout=Config.REQUEST_TIMEOUT)
#             requset_code = res.status_code
#             requset_result = res.json()
#             if requset_code == 200:
#                 return {'status': 'ok', 'message': 'SUCCESS', 'data': requset_result['data']}
#             if (
#                 '/clans/' in url
#                 and requset_code == 404
#             ):
#                 return {'status': 'ok', 'message': 'SUCCESS', 'data': {"role": None, "clan": {}, "joined_at": None, "clan_id": None}}
#             elif requset_code == 404:
#                 return {'status': 'ok', 'message': 'USER NOT EXIST'}

#             return {'status': 'error', 'message': 'NETWORK FAILURE', 'error': f'Request code:{res.status_code}'}
#         except (TimeoutException, ConnectTimeout, ReadTimeout):
#             return {'status': 'error', 'message': 'NETWORK TIMEOUT', 'error': 'Request Timeout'}


# async def get_basic_data(
#     aid: str,
#     server: str,
#     use_ac: bool = False,
#     ac: str = None
# ):
#     urls = [
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/' +
#         (f'?ac={ac}' if use_ac else '')
#     ]
#     tasks = []
#     responses = []
#     async with asyncio.Semaphore(len(urls)):
#         for url in urls:
#             tasks.append(fetch_data(url))
#         responses = await asyncio.gather(*tasks)
#         return responses
    
# async def get_basic_and_clan_data(
#     aid: str,
#     server: str,
#     use_ac: bool = False,
#     ac: str = None
# ):
#     urls = [
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/' +(f'?ac={ac}' if use_ac else ''),
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/clans/'
#     ]
#     tasks = []
#     responses = []
#     async with asyncio.Semaphore(len(urls)):
#         for url in urls:
#             tasks.append(fetch_data(url))
#         responses = await asyncio.gather(*tasks)
#         return responses

# async def get_other_data(
#     aid: str,
#     server: str,
#     use_ac: bool = False,
#     ac: str = None
# ):
#     urls = [
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/ships/pvp/' +
#         (f'?ac={ac}' if use_ac else ''),
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/ships/pvp_solo/' +
#         (f'?ac={ac}' if use_ac else ''),
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/ships/pvp_div2/' +
#         (f'?ac={ac}' if use_ac else ''),
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/ships/pvp_div3/' +
#         (f'?ac={ac}' if use_ac else ''),
#         f'{get_vortex_api_url(server=server,forward=False)}/api/accounts/{aid}/ships/rank_solo/' +
#         (f'?ac={ac}' if use_ac else '')
#     ]
#     tasks = []
#     responses = []
#     async with asyncio.Semaphore(len(urls)):
#         for url in urls:
#             tasks.append(fetch_data(url))
#         responses = await asyncio.gather(*tasks)
#         return responses

    
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

# async def main(
#     aid: str,
#     server: str,
#     lang: str,
#     use_pr: bool = True,
#     use_ac: bool = False,
#     ac: str = None
# ) -> dict:
#     parameter = [aid, server, lang, use_pr, use_ac, ac]
#     try:
#         user_data: User_Data = User_DB.get_user_data(
#             aid=aid,
#             server=server
#         )
#         user_data.query_times += 1
#         start_time = int(time.time())
#         result = {
#             'status': 'ok',
#             'message': 'SUCCESS',
#             'error': None,
#             'data': {
#                 'user': {
#                     'aid': aid,
#                     'nickname': f'RenamedUser_{aid}',
#                     'server': server,
#                     'battles': '0',
#                     'karma': '0',
#                     'registration_date': '1970/01/01',
#                     'last_battle_time': '1970/01/01',
#                     'clan_id':None,
#                     'clan_tag': None,
#                     'clan_color': None
#                 },
#                 'stats': {
#                     'overview': {},
#                     'ship_type': {},
#                     'ship_tier': {},
#                     'record': {}
#                 }
#             }
#         }
#         if str(user_data.aid) in Config.USER_BLACKLIST:
#             result['message'] = 'USER IN BLACKLIST'
#             del result['error']
#             return result
#         if  start_time - user_data.clan_update_time < Config.CLAN_CACHE_VALIDITY*24*60*60:
#             if user_data.clan_id == None:
#                 clan_basic_data = None
#                 need_update = False
#             else:
#                 clan_basic_data = Clan_DB.get_clan_basic_data(clan_id=user_data.clan_id,server=server)
#                 if start_time - clan_basic_data['update_time'] < 1*24*60*60:
#                     need_update = False
#                 else:
#                     need_update = True
#         else:
#             clan_basic_data = None
#             need_update = True
#         if need_update:
#             basic_data = await get_basic_and_clan_data(
#                 aid=aid,
#                 server=server,
#                 use_ac=use_ac,
#                 ac=ac
#             )
#             for response in basic_data:
#                 if response['status'] != 'ok' or response['message'] != 'SUCCESS':
#                     User_DB.update_user_data(user_data=user_data)
#                     return response
#             if basic_data[1]['data']['clan_id'] != None:
#                 clan_id = basic_data[1]['data']['clan_id']
#                 clan_tag = '[' + basic_data[1]['data']['clan']['tag'] + ']'
#                 clan_color = "#{:02X}{:02X}{:02X}".format(*Game_Data.clan_color[basic_data[1]['data']['clan']['color']])
#                 Clan_DB.upadte_clan_basic_data(
#                     clan_id=clan_id,
#                     server=server,
#                     clan_tag=basic_data[1]['data']['clan']['tag'],
#                     clan_color=clan_color,
#                     update_time=start_time
#                 )
#                 clan_data = {
#                     'clan_id': clan_id,
#                     'clan_tag': clan_tag,
#                     'clan_color': clan_color
#                 }
#             else:
#                 clan_id = None
#                 clan_tag = None
#                 clan_color = None
#                 clan_data = {
#                     'clan_id': clan_id,
#                     'clan_tag': 'None',
#                     'clan_color': '#B3B3B3'
#                 }
#             user_data.clan_id = clan_id
#             user_data.clan_update_time = start_time
#         else:
#             basic_data = await get_basic_data(
#                 aid=aid,
#                 server=server,
#                 use_ac=use_ac,
#                 ac=ac
#             )
#             for response in basic_data:
#                 if response['status'] != 'ok' or response['message'] != 'SUCCESS':
#                     User_DB.update_user_data(user_data=user_data)
#                     return response
#             if user_data.clan_id == None:
#                 clan_data = {
#                     'clan_id': None,
#                     'clan_tag': 'None',
#                     'clan_color': '#B3B3B3'
#                 }
#             else:
#                 clan_data = {
#                     'clan_id': clan_basic_data['clan_id'],
#                     'clan_tag': '[' + clan_basic_data['clan_tag'] + ']',
#                     'clan_color': clan_basic_data['clan_color']
#                 }
#         if (
#             user_data.clan_id != None and 
#             str(user_data.clan_id) in Config.CLAN_BLACKLIST
#         ):
#             result['message'] = 'CLAN IN BLACKLIST'
#             del result['error']
#             return result
#         nickname = basic_data[0]['data'][aid]['name']
#         if user_data.nickname != nickname:
#             user_data.nickname = nickname
#         result['data']['user']['nickname'] = nickname
#         result['data']['user']['clan_id'] = clan_data['clan_id']
#         result['data']['user']['clan_tag'] = clan_data['clan_tag']
#         result['data']['user']['clan_color'] = clan_data['clan_color']
#         if 'hidden_profile' in basic_data[0]['data'][aid]:
#             User_DB.update_user_data(user_data=user_data)
#             result['message'] = 'HIDDEN PROFILE'
#             del result['error']
#             return result
        
#         if (
#             basic_data[0]['data'][aid]['statistics'] == {} or 
#             basic_data[0]['data'][aid]['statistics']['basic'] == {}
#         ):
#             User_DB.update_user_data(user_data=user_data)
#             result['message'] = 'NO STATISTICS'
#             del result['error']
#             return result
#         basic_data = basic_data[0]['data'][aid]['statistics']['basic']
#         result['data']['user']['registration_date'] = Time_Zone.get_str_server_time_4(
#             server=server,
#             timetemp=basic_data.get('created_at',0)
#         )
#         result['data']['user']['last_battle_time'] = Time_Zone.get_str_server_time_4(
#             server=server,
#             timetemp=basic_data.get('last_battle_time',0)
#         )
#         result['data']['user']['karma'] = str(basic_data.get('karma',0))
#         result['data']['user']['battles'] = str(basic_data.get('leveling_points',0))
#         other_data = await get_other_data(
#             aid=aid,
#             server=server,
#             use_ac=use_ac,
#             ac=ac
#         )
#         for response in other_data:
#             if response['status'] != 'ok' or response['message'] != 'SUCCESS':
#                 User_DB.update_user_data(user_data=user_data)
#                 return response
#         result = other_data_processing(
#             aid=aid,
#             lang=lang,
#             server=server,
#             responses=other_data,
#             result=result
#         )
#         result = finish_data_processing(
#             use_pr=use_pr,
#             lang=lang,
#             result=result
#         )
#         User_DB.update_user_data(user_data=user_data)
#         del result['error']
#         return result
#     except Exception as e:
#         error_info = traceback.format_exc()
#         track_id = write_error(
#             error_file=__file__,
#             error_params=parameter,
#             error_name=str(type(e).__name__),
#             error_info=error_info
#         )
#         return {'status': 'error', 'message': 'PROGRAM ERROR', 'error':f'{str(type(e).__name__)}', 'track_id': f'{track_id}'}
#     finally:
#         gc.collect()
