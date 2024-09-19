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
        ...
    except Exception as e:
        traceback.print_exc()
        print(f"MySQL connection failed, error message: {e}")
    finally:
        if mysql_pool.pool != None:
            await mysql_pool.close_pool()
            print('Close the MySQL connection')

asyncio.run(test_mysql_command())