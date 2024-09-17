# -*- coding: utf-8 -*-

import aiomysql
from ..core.config import settings

class MySQLConnectionPool:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await aiomysql.create_pool(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USERNAME,
            password=settings.MYSQL_PASSWORD,
            minsize=10,
            maxsize=20
        )
    
    async def close_pool(self):
        self.pool.close()
        await self.pool.wait_closed()

mysql_pool = MySQLConnectionPool()
