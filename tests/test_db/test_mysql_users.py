# -*- coding: utf-8 -*-

import sys
import traceback
sys.path.append('F:\Kokomi_API_Main')

import asyncio
from app.db.mysql import mysql_pool
from app.api.app_electron.model.users import User_Basic_DB, User_Info_DB

async def test_user_basic():
    try:
        await mysql_pool.init_pool()
        user_db = User_Basic_DB()
        # get
        # result = await user_db.get_user_data(account_id='2023619512',region='asia')
        # update name
        # result = await user_db.update_user_name(account_id='2023619512',region='asia',nickname='SangonomiyaKokomi_')
        # update clan
        # result = await user_db.update_user_clan(account_id='2023619512',region='asia',clan_id='2000012345',clan_update_time=123456)
        # update query
        result = await user_db.update_user_query(account_id='2023619512',region='asia')
        print(result.to_dict())
    except:
        traceback.print_exc()
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

async def test_user_info():
    try:
        await mysql_pool.init_pool()
        user_db = User_Info_DB()
        result = await user_db.check_user_data(account_id='2023619512',region='asia',update_time=123456,profite=False,leveling_points=1234,last_battle_time=12345)
        print(result.to_dict())
    except:
        traceback.print_exc()
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

if __name__ == "__main__":
    asyncio.run(test_user_info())