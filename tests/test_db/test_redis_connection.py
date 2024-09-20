# -*- coding: utf-8 -*-

import sys
import traceback
sys.path.append('F:\Kokomi_API_Main')

import asyncio
from app.db.redis import redis_pool

async def test_redis_ping():
    '''
    Check whether you can successfully connect to Redis and execute the SET Key Value command
    '''
    try:
        await redis_pool.init_pool()
        redis_client = redis_pool.pool
        response = await redis_client.ping()
        if response is True:  # Redis返回True表示连接正常
            print('Redis Ping test succeeded')
    except Exception as e:
        print(f"Redis connection failed, error message: {e}")
    finally:
        if redis_pool.pool != None:
            await redis_pool.close_pool()
            print('Close the redis connection')

async def test_redis_command():
    '''
    Check whether you can successfully connect to Redis and execute the SET/GET command
    '''
    try:
        await redis_pool.init_pool()
        redis_client = redis_pool.pool
        await redis_client.execute_command("SET", "testredis1", 123, 'EX', 60)
        response = await redis_client.execute_command("GET", "testredis1")
        if response:
            print(f"Value of KEY: {response}")
        else:
            print("Key not found or expired")
    except Exception as e:
        traceback.print_exc()
        print(f"Redis connection failed, error message: {e}")
    finally:
        if redis_pool.pool != None:
            await redis_pool.close_pool()
            print('Close the redis connection')

if __name__ == "__main__":
    asyncio.run(test_redis_command())