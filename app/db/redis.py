# -*- coding: utf-8 -*-

import aioredis
from ..core.config import settings

class RedisConnectionPool:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        """
        Initialize the Redis connection pool.
        """
        self.pool = await aioredis.from_url(
            url=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            minsize=5,
            maxsize=20,
            encoding="utf-8",
            decode_responses=True
        )

    async def close_pool(self):
        """
        Close the Redis connection pool.
        """
        if self.pool:
            await self.pool.close()

redis_pool = RedisConnectionPool()
