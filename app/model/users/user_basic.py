# -*- coding: utf-8 -*-

import traceback
from typing import Dict, Any, TypedDict

import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor

from ...db.mysql import mysql_pool
from ...common.logging import API_Logging
from ...const.region import REGION_IDS
from ...schemas.responses import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class User(TypedDict):
    account_id: str
    region: str
    nickname: str
    clan_id: str | None
    clan_update_time: int
    cache_update_time: int

class User_Basic:
    def __init__(
            self, 
            account_id: str, 
            region: str, 
            nickname: str = None,
            clan_id: str = None, 
            clan_update_time: int = 0,
            cache_update_time: int = 0
        ):
        self.account_id = account_id
        self.region = region
        self.nickname = nickname if nickname else f'User_{account_id}'
        self.clan_id = clan_id
        self.clan_update_time = clan_update_time
        self.cache_update_time = cache_update_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'region': self.region,
            'nickname': self.nickname,
            'clan_id': self.clan_id ,
            'clan_update_time': self.clan_update_time,
            'cache_update_time': self.cache_update_time
        }

    def __repr__(self):
        return f"<User_Basic(account_id={self.account_id}, nickname={self.nickname}, region={self.region})>"

class User_Basic_DB:
    '''
    负责users库中user_basic表的操作，负责记录用户基本数据

    user_basic表结构：
        - account_id
        - region
        - nickname
        - clan_id
        - clan_update_time
        - cache_update_time

    *传入的region的参数是str类型，数据实际储存的是tinyint*
    '''
    @classmethod
    async def _add_user(
        self,
        user: User_Basic
    ):
        '''
        向表中插入数据
        '''
        result = None
        try:
            query = '''
            INSERT INTO user_basic (
                account_id, 
                region, 
                nickname, 
                querys, 
                clan_id, 
                clan_update_time,
                cache_update_time,
                cache_update_time
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            );
            '''
            params = (
                int(user.account_id),
                REGION_IDS.get(user.region),
                user.nickname,
                1,
                user.clan_id,
                user.clan_update_time,
                0,
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
    
    @classmethod
    async def _del_user(
        self,
        user: User_Basic
    ):
        '''
        从表中删除数据
        '''
        result = None
        try:
            query = '''
            DELETE FROM 
                user_basic 
            WHERE 
                account_id = %s AND region = %s;
            '''
            params = (
                int(user.account_id),
                REGION_IDS.get(user.region)
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
                result = InfoResponse(message='APPUSER DELETED SUCCESSFULLY')
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
    
    async def get_user_number() -> SuccessResponse | ErrorResponse:
        '''
        获取表中所有的数据的行数
        '''
        parameters = []
        result = None
        try:
            query = '''
            SELECT 
                COUNT(*)
            FROM 
                user_basic
            '''
            params = ()
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('users')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query
                    )
                    db_result = await cursor.fetchone()
                    if db_result == None or db_result == []:
                        result = SuccessResponse(
                            data = 0
                        )
                    else:
                        result = SuccessResponse(
                            data = {
                                'data_counts': db_result[0]
                            }
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
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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
        
    async def delete_user_by_aid(
        self,
        account_id: str,
        region: str
    ) -> SuccessResponse | ErrorResponse:
        '''
        删除指定用户的数据
        '''
        parameters = [account_id, region]
        result = None
        try:
            user = User_Basic(
                account_id = str(account_id),
                region = region
            )
            del_result = await self._del_user(
                user = user
            )
            if del_result.status != 'ok':
                return del_result
            result = SuccessResponse(
                data = del_result.data
            )   
            return result
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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

    async def get_user_data_by_aid(
        self,
        account_id: str,
        region: str
    ) -> SuccessResponse | ErrorResponse:
        '''
        查看指定用户的数据
        '''
        parameters = [account_id, region]
        result = None
        try:
            query = '''
            SELECT 
                user.account_id, 
                region.region, 
                user.nickname,
                user.clan_id,
                user.clan_update_time,
                user.cache_update_time
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
                REGION_IDS.get(region), 
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
                            region = region
                        )
                        result = SuccessResponse(
                            data = user
                        )
                        add_result = await self._add_user(
                            user = user
                        )
                        if add_result.status != 'ok':
                            return add_result
                    else:
                        user = User_Basic(
                            account_id=str(db_result[0]),
                            region=db_result[1],
                            nickname=db_result[2],
                            clan_id=str(db_result[3]),
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
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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

    async def hincrby_user_query_by_aid(
        self,
        account_id: str,
        region: str
    ):
        '''
        增长指定用户的query的值
        '''
        parameters = [account_id, region]
        result = None
        try:
            query = '''
            UPDATE 
                user_basic
            SET 
                querys = querys + 1
            WHERE 
                region = %s AND account_id = %s;
            '''
            params = (
                REGION_IDS.get(region),
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
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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

    async def update_user_clan_by_aid(
        self,
        account_id: str,
        region: str,
        clan_id: str,
        clan_update_time: int
    ):
        '''
        更新指定用户的clan数据
        '''
        parameters = [account_id, region, clan_id, clan_update_time]
        result = None
        try:
            query = '''
            UPDATE 
                user_basic
            SET 
                clan_id = %s,
                clan_update_time = %s
            WHERE 
                region = %s AND account_id = %s;
            '''
            params = (
                int(clan_id),
                clan_update_time,
                REGION_IDS.get(region),
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
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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
        
    async def update_user_name_by_aid(
        self,
        account_id: str,
        region: str,
        nickname: str
    ):
        '''
        更新指定用户的游戏名称
        '''
        parameters = [account_id, region, nickname]
        result = None
        try:
            query = '''
            UPDATE 
                user_basic
            SET 
                nickname = %s
            WHERE 
                region = %s AND account_id = %s;
            '''
            params = (
                nickname,
                REGION_IDS.get(region),
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
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameters,
                error_name=str(type(e).__name__),
                error_info=error_info
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