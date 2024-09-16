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
            minsize=1,
            maxsize=20
        )

    async def fetch_all(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
                return result

    async def fetch_one(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchone()
                return result

    async def execute(self, query, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()

mysql_pool = MySQLConnectionPool()
