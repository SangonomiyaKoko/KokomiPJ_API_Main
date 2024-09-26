# -*- coding: utf-8 -*-

import sys
import traceback
sys.path.append('F:\Kokomi_API_Main')

import asyncio
from app.db.mysql import mysql_pool
from app.api.app_electron.model.clans import Clan_Basic_DB

async def test_users_get_user():
    try:
        await mysql_pool.init_pool()
        clan_db = Clan_Basic_DB()
        # get
        result = await clan_db.get_clan_data(clan_id='2000012345', region='asia')
        # update clan
        # result = await clan_db.update_clan_info(clan_id='2000012345', region='asia', clan_tag='TEST', clan_color=0, update_time=123456)
        
        print(result.to_dict())
    except:
        traceback.print_exc()
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

if __name__ == "__main__":
    asyncio.run(test_users_get_user())