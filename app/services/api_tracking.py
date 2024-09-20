import time
import traceback
from aioredis.client import Redis
from . import redis_pool, API_Logging

exists_huorly_key = []
exists_daily_key = []

class API_Tracker:
    def __init__(self):
        self.__hourly_key = "api_calls:hourly"
        self.__daily_key = "api_calls:daily"
    
    def __add_hourly_key(self, key):
        exists_huorly_key.append(key)
        if len(exists_huorly_key) > 25:
            self.__del_hourly_key()
    
    def __del_hourly_key(self):
        del exists_huorly_key[0]

    def __add_daily_key(self, key):
        exists_daily_key.append(key)
        if len(exists_daily_key) > 31:
            self.__del_daily_key()
    
    def __del_daily_key(self):
        del exists_daily_key[0]

    async def record_api_call(self):
        """
        Record the current interface calls to Redis and update the number of requests per hour and day.
        """
        try:
            params = []
            redis_client: Redis = redis_pool.pool
            current_time = int(time.time())
            current_hour = time.strftime('%Y-%m-%d-%H', time.gmtime(current_time))
            current_day = time.strftime('%Y-%m-%d', time.gmtime(current_time))
            hourly_key = f"{self.__hourly_key}:{current_hour}"
            daily_key = f"{self.__daily_key}:{current_day}"
            async with redis_client.pipeline() as pipe:
                pipe.execute_command("HINCRBY", hourly_key, 'total', 1)
                pipe.execute_command("HINCRBY", daily_key, 'total', 1)
                params.append(["HINCRBY", hourly_key, 'total', 1])
                params.append(["HINCRBY", daily_key, 'total', 1])
                if hourly_key not in exists_huorly_key:
                    pipe.execute_command("EXPIRE", hourly_key, 25*60*60)
                    self.__add_hourly_key(hourly_key)
                    params.append(["EXPIRE", hourly_key, 25*60*60])
                if daily_key not in exists_daily_key:
                    pipe.execute_command("EXPIRE", daily_key, 31*24*60*60)
                    self.__add_daily_key(daily_key)
                    params.append(["EXPIRE", daily_key, 31*24*60*60])
                a = await pipe.execute()
                return a
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_redis_error(
                error_file=__file__,
                error_name=f'REDIS_ERROR_{type(e).__name__}',
                error_params=str(params),
                error_info=error_info,
            )
