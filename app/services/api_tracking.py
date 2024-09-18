import time
from datetime import datetime
from ..db.redis import redis_pool

class ApiTracker:
    def __init__(self):
        self.hourly_key = "api_calls_hourly"
        self.daily_key = "api_calls_daily"
        self.expire_time = 24 * 60 * 60
        self.days_7_expire_time = 7 * 24 * 60 * 60

    async def record_api_call(self):
        """
        记录当前接口调用的时间戳到 Redis，更新每小时和每天的请求数。
        """
        redis_client = redis_pool.pool
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        current_day = datetime.now().strftime('%Y-%m-%d')
        await redis_client.hincrby(self.hourly_key, current_hour, 1)
        await redis_client.expire(self.hourly_key, self.expire_time)
        await redis_client.hincrby(self.daily_key, current_day, 1)
        await redis_client.expire(self.daily_key, self.days_7_expire_time)

    async def get_hourly_api_call_counts(self):
        """
        获取过去24小时每小时的接口调用次数。
        """
        redis_client = redis_pool.pool
        counts = {}
        for i in range(24):
            # 获取每小时的时间戳
            past_hour = datetime.now().replace(minute=0, second=0, microsecond=0).timestamp() - i * 3600
            hour_key = datetime.fromtimestamp(past_hour).strftime('%Y-%m-%d-%H')
            # 获取该小时的请求数
            count = await redis_client.hget(self.hourly_key, hour_key)
            counts[hour_key] = int(count) if count else 0
        return counts

    async def get_daily_api_call_counts(self):
        """
        获取过去7天每天的接口调用次数。
        """
        redis_client = redis_pool.pool
        counts = {}
        for i in range(7):
            past_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() - i * 86400
            day_key = datetime.fromtimestamp(past_day).strftime('%Y-%m-%d')
            count = await redis_client.hget(self.daily_key, day_key)
            counts[day_key] = int(count) if count else 0
        return counts
