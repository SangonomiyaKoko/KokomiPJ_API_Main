import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor
from typing import Dict, Any
from .. import API_Logging, mysql_pool
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class User_Basic:
    def __init__(
            self, 
            account_id, 
            region, 
            nickname=None, 
            querys=0, 
            clan_id=None, 
            clan_update_time=0
        ):
        self.account_id = account_id
        self.region = region
        self.nickname = nickname if nickname else f'RenamedUser_{account_id}'
        self.querys = querys
        self.clan_id = clan_id
        self.clan_update_time = clan_update_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'region': self.region,
            'nickname': self.nickname,
            'querys': self.querys ,
            'clan_id': self.clan_id ,
            'clan_update_time': self.clan_update_time
        }

    def __repr__(self):
        return f"User_Basic(account_id={self.account_id}, nickname={self.nickname}, region={self.region})"

class User_Basic_DB:
    async def get_user_db(
        self,
        account_id: str
    ):
        try:
            result = None
            query = '''
            SELECT 
                u.account_id, 
                s.region, 
                u.nickname,
                u.querys,
                u.clan_id,
                u.clan_update_time
            FROM 
                user_basic u
            JOIN 
                servers s
            ON 
                u.server = s.id
            WHERE
                u.account_id = %s
            '''
            params = (account_id,)
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
                            account_id=db_result[0],
                            region=db_result[1]
                        )
                        result = SuccessResponse(
                            data = user
                        )
                        self.add_user_db(
                            user=user
                        )
                    else:
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
    
    async def add_user_db(
        self,
        user: User_Basic
    ):
        try:
            result = None
            query = '''
            INSERT INTO accounts (
                account_id, 
                region, 
                nickname, 
                querys, 
                clan_id, 
                clan_update_time
            )
            VALUES (%s, %s, %s, %s, %s, %s);

            '''
            params = (user.account_id,user.region,user.nickname,user.querys,user.clan_id,user.clan_update_time)
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

    def update_user_db():
        ...

