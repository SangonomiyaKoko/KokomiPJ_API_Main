import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor
from typing import Dict, Any, Optional, TypedDict
from .. import API_Logging, mysql_pool, REGION_IDS
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

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

class User_Info:
    def __init__(
            self, 
            account_id: str, 
            region: str, 
            update_time: int = 0,
            profite: bool = False, 
            leveling_points: int = 0,
            last_battle_time: int = 0
        ):
        self.account_id = account_id
        self.region = region
        self.update_time = update_time
        self.profite = profite
        self.leveling_points = leveling_points
        self.last_battle_time = last_battle_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'account_id': self.account_id,
            'region': self.region,
            'profite': self.profite,
            'profite': self.profite,
            'leveling_points': self.leveling_points,
            'last_battle_time': self.last_battle_time
        }

    def __repr__(self):
        return f"<User_Info(account_id={self.account_id}, region={self.region})>"

class User_Basic_DB:
    async def get_user_data(
        self,
        account_id: str,
        region: str
    ) -> SuccessResponse | ErrorResponse:
        try:
            result = None
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
    
    async def _add_user(
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

    async def update_user_query(
        self,
        account_id: str,
        region: str
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

    async def update_user_clan(
        self,
        account_id: str,
        region: str,
        clan_id: str,
        clan_update_time: int
    ):
        try:
            result = None
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
        
    async def update_user_name(
        self,
        account_id: str,
        region: str,
        nickname: str
    ):
        try:
            result = None
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

class User_Info_DB:
    async def check_user_data(
        self,
        account_id: str,
        region: str,
        update_time: int,
        profite: bool,
        leveling_points: int,
        last_battle_time: int
    ) -> SuccessResponse | ErrorResponse:
        try:
            result = None
            query = '''
            SELECT 
                user.account_id, 
                region.region, 
                user.update_time,
                user.profite,
                user.leveling_points,
                user.last_battle_time
            FROM 
                user_info user
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
                        query = '''
                        INSERT INTO user_info (
                            account_id, 
                            region, 
                            update_time, 
                            profite, 
                            leveling_points, 
                            last_battle_time
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s
                        );
                        '''
                        params = (
                            int(account_id),
                            REGION_IDS.get(region),
                            update_time,
                            profite,
                            leveling_points,
                            last_battle_time
                        )
                        await cursor.execute(
                            query,
                            params
                        )
                    else:
                        if not all(
                            [
                                db_result[3] == profite,
                                db_result[4] == leveling_points,
                                db_result[5] == last_battle_time
                            ]
                        ):
                            query = '''
                            UPDATE 
                                user_info
                            SET 
                                update_time = %s,
                                profite = %s,
                                leveling_points = %s,
                                last_battle_time = %s
                            WHERE 
                                region = %s AND account_id = %s;
                            '''
                            params = (
                                update_time,
                                profite,
                                leveling_points,
                                last_battle_time,
                                REGION_IDS.get(region),
                                int(account_id)
                            )
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