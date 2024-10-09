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

class User_Info_DB:
    '''
    负责users库中user_info表的操作，负责记录用户详细数据

    用于recent/recents/cache功能的更新逻辑

    user_basic表结构：
        - account_id
        - region
        - update_time
        - profite
        - leveling_points
        - last_battle_time

    *传入的region的参数是str类型，数据实际储存的是tinyint*
    '''
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