import time
from datetime import datetime
from ..db.redis import redis_pool

class ApiTracker:
    def __init__(self):
        self.hourly_key = "api_calls_hourly"
        self.daily_key = "api_calls_daily"
        self.hour_expire_time = 60 * 60
        self.days_expire_time = 30 * 24 * 60 * 60

    async def record_api_call(self):
        """
        记录当前接口调用的时间戳到 Redis，更新每小时和每天的请求数。
        """
        redis_client = redis_pool.pool
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        current_day = datetime.now().strftime('%Y-%m-%d')
        await redis_client.execute_command()
