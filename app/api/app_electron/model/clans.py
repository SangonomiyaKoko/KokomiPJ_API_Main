import aiomysql
from aiomysql.pool import Pool
from aiomysql.connection import Connection
from aiomysql.cursors import Cursor
from typing import Dict, Any, TypedDict
from .. import API_Logging, mysql_pool, REGION_IDS
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class Clan(TypedDict):
    clan_id: str
    region: str
    clan_tag: str | None
    clan_color: str | None
    update_time: int

class Clan_Basic:
    def __init__(
            self, 
            clan_id: str, 
            region: str, 
            clan_tag: str = None,
            clan_color: int = None, 
            update_time: int = 0
        ):
        self.clan_id = clan_id
        self.region = region
        self.clan_tag = clan_tag if clan_tag else 'UNDEFINED'
        self.clan_color = clan_color
        self.update_time = update_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'clan_id': self.clan_id,
            'region': self.region,
            'clan_tag': self.clan_tag,
            'clan_color': self.clan_color ,
            'update_time': self.update_time
        }

    def __repr__(self):
        return f"<Clan_Basic(clan_id={self.clan_id}, clan_tag={self.clan_tag}, region={self.region})>"
    

class Clan_Basic_DB:
    async def get_clan_data(
        self,
        clan_id: str,
        region: str
    ):
        try:
            result = None
            query = '''
            SELECT 
                clan.clan_id, 
                region.region, 
                clan.clan_tag,
                clan.clan_color,
                clan.update_time
            FROM 
                clan_basic clan
            JOIN 
                servers region
            ON 
                clan.region = region.id
            WHERE
                clan.region = %s AND clan.clan_id = %s
            '''
            params = (
                REGION_IDS.get(region), 
                int(clan_id)
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('clans')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                    db_result = await cursor.fetchone()
                    if db_result == None or db_result == []:
                        clan = Clan_Basic(
                            clan_id=clan_id,
                            region=region
                        )
                        result = SuccessResponse(
                            data = clan
                        )
                        add_result = await self._add_clan(
                            clan=clan
                        )
                        if add_result.status != 'ok':
                            return add_result
                    else:
                        user = Clan_Basic(
                            clan_id=str(db_result[0]),
                            region=db_result[1],
                            clan_tag=db_result[2],
                            clan_color=db_result[3],
                            update_time=db_result[4]
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
    
    async def _add_clan(
        self,
        clan: Clan_Basic
    ):
        try:
            result = None
            query = '''
            INSERT INTO clan_basic (
                clan_id, 
                region, 
                clan_tag, 
                clan_color,
                update_time
            )
            VALUES (
                %s, %s, %s, %s, %s
            );
            '''
            params = (
                int(clan.clan_id),
                REGION_IDS.get(clan.region),
                clan.clan_tag,
                clan.clan_color,
                clan.update_time
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('clans')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                await conn.commit()
                result = InfoResponse(message='APPCLAN ADDED SUCCESSFULLY')
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
        
    async def update_clan_info(
        self,
        clan_id: str,
        region: str,
        clan_tag: str,
        clan_color: int,
        update_time: int
    ):
        try:
            result = None
            query = '''
            UPDATE 
                clan_basic
            SET 
                clan_tag = %s,
                clan_color = %s,
                update_time = %s
            WHERE 
                region = %s AND clan_id = %s;
            '''
            params = (
                clan_tag,
                clan_color,
                update_time,
                REGION_IDS.get(region),
                int(clan_id)
            )
            mysql_client: Pool = mysql_pool.pool
            async with mysql_client.acquire() as conn:
                conn: Connection
                await conn.select_db('clans')
                async with conn.cursor() as cursor:
                    cursor: Cursor
                    await cursor.execute(
                        query,
                        params
                    )
                await conn.commit()
                result = InfoResponse(message='APPCLAN UPDATE SUCCESSFULLY')
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