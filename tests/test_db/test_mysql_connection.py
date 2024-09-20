# -*- coding: utf-8 -*-

import sys
import traceback
sys.path.append('F:\Kokomi_API_Main')

import asyncio
from app.db.mysql import mysql_pool

async def test_mysql_command():
    '''
    Check whether you can successfully connect to MySQL and execute the SELECT command
    '''
    try:
        await mysql_pool.init_pool()
        mysql_client = mysql_pool.pool
        query = '''
        SELECT VERSION();
        '''
        async with mysql_client.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query
                )
                db_result = await cursor.fetchone()
                print(db_result)
    except Exception as e:
        traceback.print_exc()
        print(f"MySQL connection failed, error message: {e}")
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

if __name__ == "__main__":
    asyncio.run(test_mysql_command())