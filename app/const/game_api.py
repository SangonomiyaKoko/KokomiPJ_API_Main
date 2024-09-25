# -*- coding: utf-8 -*-

from ..core.config import settings

'''
This is used to store some game-related constant data
'''
class API_CONST:
    VORTEX_API_URL = {
        'asia': 'http://vortex.worldofwarships.asia',
        'eu': 'http://vortex.worldofwarships.eu',
        'na': 'http://vortex.worldofwarships.com',
        'ru': 'http://vortex.korabli.su',
        'cn': 'http://vortex.wowsgame.cn'
    }

    OFFICIAL_API_URL = {
        'asia': 'https://api.worldofwarships.asia',
        'eu': 'https://api.worldofwarships.eu',
        'na': 'https://api.worldofwarships.com',
        'ru': 'https://api.korabli.su',
        'cn': None
    }

    CLAN_API_URL = {
        'asia': 'https://clans.worldofwarships.asia',
        'eu': 'https://clans.worldofwarships.eu',
        'na': 'https://clans.worldofwarships.com',
        'ru': 'https://clans.korabli.su',
        'cn': 'https://clans.wowsgame.cn'
    }

    OFFICIAL_API_TOKEN = {
        'asia': settings.WG_API_TOKEN,
        'eu': settings.WG_API_TOKEN,
        'na': settings.WG_API_TOKEN,
        'ru': settings.LESTA_API_TOKEN,
        'cn': settings.CN_API_TOKEN
    }