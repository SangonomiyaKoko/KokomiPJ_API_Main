# -*- coding: utf-8 -*-

import traceback

import asyncio
from app.services.api_tracking import API_Tracker
from app.db.redis import redis_pool

async def test_api_tracking():
    try:
        await redis_pool.init_pool()
        await API_Tracker().record_api_call()
    except:
        traceback.print_exc()
    finally:
        print(type(redis_pool.pool))
        if redis_pool.pool != None:
            await redis_pool.close_pool()
            print('Close the redis connection')

if __name__ == "__main__":
    asyncio.run(test_api_tracking())