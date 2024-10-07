# -*- coding: utf-8 -*-

#  TODO: Some commonly used tool functions, such as string processing, encryption and decryption, time formatting, etc
import json
import os
from typing import TypedDict

from .. import PROJECT_PATH
from ..const.game_data import GAME_CONST

class Personal_Rating:
    def get_pr_by_sid_and_region(
        sid: str,
        region: str,
        battle_type: str,
        ship_data: list
    ):
        '''
        计算船只数据的pr
        ship_data [battles,wins,damage,frag]
        '''
        result = {
            'value_battles_count': 0,
            'personal_rating': -1,
            'n_damage_dealt': -1,
            'n_frags': -1
        }
        battles_count = ship_data[0]
        if battles_count <= 0:
            return result
        # 获取服务器数据
        ship_data_class = Ship_Data()
        server_data = ship_data_class.get_data_by_sid_and_region(
            sid=sid,
            region=region
        )
        if server_data == {}:
            return result
        # 用户数据
        actual_wins = ship_data[1] / battles_count * 100
        actual_dmg = ship_data[2] / battles_count
        actual_frags = ship_data[3] / battles_count
        # 服务器数据
        server_data: Ship_Data_Dict = server_data[sid]
        expected_wins = server_data['win_rate']
        expected_dmg = server_data['avg_damage']
        expected_frags = server_data['avg_frags']
        # 计算PR
        # Step 1 - ratios:
        r_wins = actual_wins / expected_wins
        r_dmg = actual_dmg / expected_dmg
        r_frags = actual_frags / expected_frags
        # Step 2 - normalization:
        n_wins = max(0, (r_wins - 0.7) / (1 - 0.7))
        n_dmg = max(0, (r_dmg - 0.4) / (1 - 0.4))
        n_frags = max(0, (r_frags - 0.1) / (1 - 0.1))
        # Step 3 - PR value:
        if battle_type in ['rank', 'rank_solo']:
            personal_rating = 600 * n_dmg + 350 * n_frags + 400 * n_wins
        else:
            personal_rating = 700 * n_dmg + 300 * n_frags + 150 * n_wins
        result['value_battles_count'] = battles_count
        result['personal_rating'] = round(personal_rating * battles_count, 6)
        result['n_damage_dealt'] = round((actual_dmg / expected_dmg) * battles_count, 6)
        result['n_frags'] = round((actual_frags / expected_frags) * battles_count, 6)
        return result

class Ship_Data_Dict(TypedDict):
    battles_count: int
    win_rate: int
    avg_damage: int
    avg_frags: int
    avg_exp: int
    survived_rate: int
    avg_scouting_damage: int
    avg_art_agro: int
    avg_planes_killed: int

class Ship_Data:
    _instance = None
    _ship_data: dict = {}
    _ship_update: int = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_data()
        return cls._instance

    @classmethod
    def _load_data(cls):
        with open(
            file=os.path.join(PROJECT_PATH, 'json', 'ship_data.json'), 
            mode='r',
            encoding='utf-8'
        ) as f:
            data: dict = json.load(f)
            cls._ship_data = data.get('ship_data', {})
            cls._ship_update = data.get('update_time', 0)

    def get_data_update(self) -> int:
        return self._ship_update

    def get_data_by_sid(
        self,
        sid: str
    ) -> dict:
        '''
        获取指定船只的服务器数据
        '''
        result = {}
        ship_data: dict | None = self._ship_data.get(sid, None)
        if ship_data:
            result[sid] = ship_data
        return result
    
    def get_data_by_sids(
        self,
        sids: list
    ) -> dict:
        '''
        获取指定船只列表的服务器数据
        '''
        result = {}
        for sid in sids:
            ship_data: dict | None = self._ship_data.get(sid, None)
            if ship_data:
                result[sid] = ship_data
        return result
        

    def get_data_by_sid_and_region(
        self,
        sid: str,
        region: str
    ) -> dict:
        '''
        获取指定船只和指定服务器的服务器数据
        '''
        result = {}
        ship_data: dict | None = self._ship_data.get(sid, None)
        if ship_data:
            result = {}
            result[sid] = ship_data.get(region, None)
        return result
    
    def get_data_by_sids_and_region(
        self,
        sids: list,
        region: str
    ) -> dict:
        '''
        获取指定船只列表和指定服务器的服务器数据
        '''
        result = {}
        for sid in sids:
            ship_data: dict | None = self._ship_data.get(sid, None)
            if ship_data:
                result = {}
                result[sid] = ship_data.get(region, None)
        return result
        
class Ship_Info_Dict(TypedDict):
    ship_tier: int
    ship_type: str
    ship_nation: str
    premium: bool
    special: bool
    ship_name: str | dict
    ship_index: str
    ship_server: str

class Ship_Info:
    _instance = None
    _data_main: dict = {}
    _data_nick: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_data()
        return cls._instance

    @classmethod
    def _load_data(cls):
        with open(
            file=os.path.join(PROJECT_PATH, 'json', 'ship_name_main.json'), 
            mode='r',
            encoding='utf-8'
        ) as f:
            data: dict = json.load(f)
            cls._data_main = data

        with open(
            file=os.path.join(PROJECT_PATH, 'json', 'ship_name_nick.json'), 
            mode='r',
            encoding='utf-8'
        ) as f:
            data: dict = json.load(f)
            cls._data_nick = data

    def get_data_by_sid(
        self,
        sid: str,
        region: str
    ) -> dict:
        '''
        获取指定船只的详细数据
        '''
        result = {}
        if region == 'ru' and sid == '3550394128':
            ship_name_data = self._data_main
            result[sid] = {
                'ship_tier':ship_name_data['3550394129']['tier'],
                'ship_type':ship_name_data['3550394129']['type'],
                'ship_nation':ship_name_data['3550394129']['nation'],
                'premium':ship_name_data['3550394129']['premium'],
                'special':ship_name_data['3550394129']['special'],
                'ship_name':ship_name_data['3550394129']['ship_name'],
                'ship_index':ship_name_data['3550394129']['index'],
                'ship_server':ship_name_data['3550394129']['server']
            }
        else:
            ship_name_data = self._data_main.get(sid, None)
            if ship_name_data:
                result[sid] = {
                    'ship_tier':ship_name_data['tier'],
                    'ship_type':ship_name_data['type'],
                    'ship_nation':ship_name_data['nation'],
                    'premium':ship_name_data['premium'],
                    'special':ship_name_data['special'],
                    'ship_name':ship_name_data['ship_name'],
                    'ship_index':ship_name_data['index'],
                    'ship_server':ship_name_data['server']
                }
        return result

    def get_data_by_sid_and_lang(
        self,
        sid: str,
        region: str,
        lang: str
    ) -> dict:
        '''
        获取指定船只和指定语言的详细数据
        '''
        result = {}
        if region == 'ru' and sid == '3550394128':
            ship_name_data = self._data_main
            result[sid] = {
                'ship_tier':ship_name_data['3550394129']['tier'],
                'ship_type':ship_name_data['3550394129']['type'],
                'ship_nation':ship_name_data['3550394129']['nation'],
                'premium':ship_name_data['3550394129']['premium'],
                'special':ship_name_data['3550394129']['special'],
                'ship_name':ship_name_data['3550394129']['ship_name'][lang],
                'ship_index':ship_name_data['3550394129']['index'],
                'ship_server':ship_name_data['3550394129']['server']
            }
        else:
            ship_name_data = self._data_main.get(sid, None)
            if ship_name_data:
                result[sid] = {
                    'ship_tier':ship_name_data['tier'],
                    'ship_type':ship_name_data['type'],
                    'ship_nation':ship_name_data['nation'],
                    'premium':ship_name_data['premium'],
                    'special':ship_name_data['special'],
                    'ship_name':ship_name_data['ship_name'][lang],
                    'ship_index':ship_name_data['index'],
                    'ship_server':ship_name_data['server']
                }
        return result
    
    def get_data_by_sids_and_lang(
        self,
        sids: list,
        region: str,
        lang: str
    ) -> dict:
        '''
        获取指定船只列表和指定语言的详细数据
        '''
        result = {}
        for sid in sids:
            if region == 'ru' and sid == '3550394128':
                ship_name_data = self._data_main
                result[sid] = {
                    'ship_tier':ship_name_data['3550394129']['tier'],
                    'ship_type':ship_name_data['3550394129']['type'],
                    'ship_nation':ship_name_data['3550394129']['nation'],
                    'premium':ship_name_data['3550394129']['premium'],
                    'special':ship_name_data['3550394129']['special'],
                    'ship_name':ship_name_data['3550394129']['ship_name'][lang],
                    'ship_index':ship_name_data['3550394129']['index'],
                    'ship_server':ship_name_data['3550394129']['server']
                }
            else:
                ship_name_data = self._data_main.get(sid, None)
                if ship_name_data:
                    result[sid] = {
                        'ship_tier':ship_name_data['tier'],
                        'ship_type':ship_name_data['type'],
                        'ship_nation':ship_name_data['nation'],
                        'premium':ship_name_data['premium'],
                        'special':ship_name_data['special'],
                        'ship_name':ship_name_data['ship_name'][lang],
                        'ship_index':ship_name_data['index'],
                        'ship_server':ship_name_data['server']
                    }
        return result
    
    def name_format(
        self,
        input_name: str
    ) -> str:
        name_list = input_name.split()
        input_name = None
        input_name = ''.join(name_list)
        en_list = {
            'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
            'e': ['è', 'é', 'ê', 'ë'],
            'i': ['ì', 'í', 'î', 'ï'],
            'o': ['ó', 'ö', 'ô', 'õ', 'ò', 'ō'],
            'u': ['ü', 'û', 'ú', 'ù', 'ū'],
            'y': ['ÿ', 'ý']
        }
        for en, lar in en_list.items():
            for index in lar:
                if index in input_name:
                    input_name = input_name.replace(index, en)
                if index.upper() in input_name:
                    input_name = input_name.replace(index.upper(), en.upper())
        re_str = ['_', '-', '·', '.', '\'','(',')','（','）']
        for index in re_str:
            if index in input_name:
                input_name = input_name.replace(index, '')
        input_name = input_name.lower()
        return input_name

    def format_result(
        self,
        result: dict,
        main_data: dict,
        ship_id: str
    ):
        if ship_id == '3550394129':
            result['3550394128'] = {
                'ship_tier': main_data[ship_id]['tier'],
                'ship_type': main_data[ship_id]['type'],
                'ship_nation': main_data[ship_id]['nation'],
                'premium': main_data[ship_id]['premium'],
                'special': main_data[ship_id]['special'],
                'ship_name': main_data[ship_id]['ship_name'],
                'ship_index': main_data[ship_id]['index'],
                'ship_server': main_data[ship_id]['server']
            }
        else:
            result[ship_id] = {
                'ship_tier': main_data[ship_id]['tier'],
                'ship_type': main_data[ship_id]['type'],
                'ship_nation': main_data[ship_id]['nation'],
                'premium': main_data[ship_id]['premium'],
                'special': main_data[ship_id]['special'],
                'ship_name': main_data[ship_id]['ship_name'],
                'ship_index': main_data[ship_id]['index'],
                'ship_server': main_data[ship_id]['server']
            }
        return result

    def search_ship(
        self,
        ship_name: str,
        lang: str
    ):
        '''
        搜索输入的船只名称，首先采用完全匹配，匹配不到则采用模糊匹配

        '''
        result = {}
        ship_name_format = self.name_format(ship_name)
        ship_name_len = len(ship_name_format)
        if (
            'old' in ship_name_format[ship_name_len-3:] or 
            '旧' in ship_name_format[ship_name_len-3:]
        ):
            old = True
        else:
            old = False
        nick_data = self._data_main
        main_data = self._data_nick
        # 完全匹配, 昵称
        for ship_id, ship_data in nick_data[lang].items():
            for index in ship_data:
                if ship_name_format == self.name_format(index):
                    result = self.format_result(
                        result=result,
                        main_data=main_data,
                        ship_id=ship_id
                    )
                    return result
        # 完全匹配, 官方名称
        for ship_id, ship_data in main_data.items():
            if ship_name_format == self.name_format(ship_data['ship_name']['en']):
                result = self.format_result(
                    result=result,
                    main_data=main_data,
                    ship_id=ship_id
                )
                return result
            if lang in ['cn','ja']:
                if ship_name_format == self.name_format(ship_data['ship_name'][lang]):
                    result = self.format_result(
                        result=result,
                        main_data=main_data,
                        ship_id=ship_id
                    )
                    return result
        # 模糊匹配, 官方名称
        for ship_id, ship_data in main_data.items():
            if ship_name_format in self.name_format(ship_data['ship_name']['en']):
                if old == False and ship_id in GAME_CONST.OLD_SHIP_LIST:
                    continue
                result = self.format_result(
                    result=result,
                    main_data=main_data,
                    ship_id=ship_id
                )
            if lang in ['cn','ja']:
                if ship_name_format in self.name_format(ship_data['ship_name'][lang]):
                    if old == False and ship_id in GAME_CONST.OLD_SHIP_LIST:
                        continue
                    result = self.format_result(
                        result=result,
                        main_data=main_data,
                        ship_id=ship_id
                    )
        return result