# -*- coding: utf-8 -*-

import sys
import traceback
sys.path.append('F:\Kokomi_API_Main')

import asyncio
from app.db.mysql import mysql_pool
from app.api.app_electron.model.user import User_Basic_DB

async def test_users_get_user():
    try:
        await mysql_pool.init_pool()
        user_db = User_Basic_DB()
        result = await user_db.update_user_query(account_id='2023619512',server='asia')
        print(result.to_dict())
    except:
        traceback.print_exc()
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

if __name__ == "__main__":
    asyncio.run(test_users_get_user())