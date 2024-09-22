import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor
from typing import Dict, Any
from .. import API_Logging, mysql_pool, REGION_IDS
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class User_Basic:
    def __init__(
            self, 
            account_id, 
            region, 
            nickname=None,
            clan_id=None, 
            clan_update_time=0
        ):
        self.account_id = account_id
        self.region = region
        self.nickname = nickname if nickname else 'UNDEFINED'
        self.clan_id = clan_id
        self.clan_update_time = clan_update_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'region': self.region,
            'nickname': self.nickname,
            'clan_id': self.clan_id ,
            'clan_update_time': self.clan_update_time
        }

    def __repr__(self):
        return f"<User_Basic(account_id={self.account_id}, nickname={self.nickname}, region={self.region})>"

class User_Basic_DB:
    async def get_user_data(
        self,
        account_id: str,
        server: str
    ):
        try:
            result = None
            query = '''
            SELECT 
                user.account_id, 
                region.region, 
                user.nickname,
                user.clan_id,
                user.clan_update_time
            FROM 
                user_basic user
            JOIN 
                servers region
            ON 
                user.region = region.id
            WHERE
                user.region = %s AND user.account_id = %s
            '''
            params = (
                REGION_IDS.get(server), 
                int(account_id)
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('users')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                    db_result = await cursor.fetchone()
                    if db_result == None or db_result == []:
                        user = User_Basic(
                            account_id = str(account_id),
                            region = server
                        )
                        result = SuccessResponse(
                            data = user
                        )
                        add_result = await self.__add_user(
                            user = user
                        )
                        if add_result.status != 'ok':
                            return add_result
                    else:
                        user = User_Basic(
                            account_id=str(db_result[0]),
                            region=db_result[1],
                            nickname=db_result[2],
                            clan_id=db_result[3],
                            clan_update_time=db_result[4]
                        )
                        result = SuccessResponse(
                            data = user
                        )
                    return result 
        except aiomysql.MySQLError as e:
            track_id = API_Logging().write_mysql_error(
                error_file=__file__,
                error_code=f'MYSQL_ERROR_{e.args[0]}',
                error_info=str(e.args[1]),
                error_query=query,
                error_data=str(params)
            )
            error = BaseError(
                error_info=str(type(e).__name__),
                track_id=track_id
            )
            result = ErrorResponse(
                message='PROGRAM ERROR',
                data=error
            )
            return result
    
    async def __add_user(
        self,
        user: User_Basic
    ):
        try:
            result = None
            query = '''
            INSERT INTO user_basic (
                account_id, 
                region, 
                nickname, 
                querys, 
                clan_id, 
                clan_update_time,
                cache_update_time
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s
            );
            '''
            params = (
                int(user.account_id),
                REGION_IDS.get(user.region),
                user.nickname,
                1,
                user.clan_id,
                user.clan_update_time,
                0
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('users')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                await conn.commit()
                result = InfoResponse(message='APPUSER ADDED SUCCESSFULLY')
                return result
        except aiomysql.MySQLError as e:
            track_id = API_Logging().write_mysql_error(
                error_file=__file__,
                error_code=f'MYSQL_ERROR_{e.args[0]}',
                error_info=str(e.args[1]),
                error_query=query,
                error_data=str(params)
            )
            error = BaseError(
                error_info=str(type(e).__name__),
                track_id=track_id
            )
            result = ErrorResponse(
                message='PROGRAM ERROR',
                data=error
            )
            return result

    async def update_user_query(
        self,
        account_id: str,
        server: str
    ):
        try:
            result = None
            query = '''
            UPDATE 
                user_basic
            SET 
                querys = querys + 1
            WHERE 
                region = %s AND account_id = %s;
            '''
            params = (
                REGION_IDS.get(server),
                int(account_id)
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('users')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                await conn.commit()
                result = InfoResponse(message='APPUSER UPDATE SUCCESSFULLY')
                return result
        except aiomysql.MySQLError as e:
            track_id = API_Logging().write_mysql_error(
                error_file=__file__,
                error_code=f'MYSQL_ERROR_{e.args[0]}',
                error_info=str(e.args[1]),
                error_query=query,
                error_data=str(params)
            )
            error = BaseError(
                error_info=str(type(e).__name__),
                track_id=track_id
            )
            result = ErrorResponse(
                message='PROGRAM ERROR',
                data=error
            )
            return result

class User_Info_DB:
    ...