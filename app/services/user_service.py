import aiomysql
from typing import Dict, Any
from . import mysql_pool, API_Logging
from . import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class API_Auth:
    async def add_user(
        username: str, 
        password: str, 
        roles: str
    ) -> InfoResponse | ErrorResponse:
        try:
            result = None
            query = '''
            INSERT INTO api_users (username, password, role)
            VALUES (%s, %s, %s)
            '''
            params = (username, password, roles)
            async with mysql_pool.pool.acquire() as conn:
                await conn.select_db('auth_db')
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        query, 
                        params
                    )
                    await conn.commit()
            result = InfoResponse(message='APIUSER ADDED SUCCESSFULLY')
            return result
        except aiomysql.MySQLError as e:
            if e.args[0] == 1062:
                result = InfoResponse(message='APIUSER ALREADY EXISTS')
                return result
            else:
                track_id = API_Logging().write_mysql_error(
                    error_file=__file__,
                    error_code=f'MYSQL_ERROR_{e.args[0]}',
                    error_info=str(e.args[1]),
                    error_query=query,
                    error_data=str(params),
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
    
    async def get_user(
        username: str
    ) -> SuccessResponse | ErrorResponse:
        try:
            result = None
            query = '''
            SELECT username, password, role
            FROM api_users
            WHERE username = %s
            '''
            params = (username,)
            async with mysql_pool.pool.acquire() as conn:
                await conn.select_db('auth_db')
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        query,
                        params
                    )
                    db_result = await cursor.fetchone()
                    if db_result == None or db_result == []:
                        result = SuccessResponse(
                            data = {}
                        )
                    else:
                        result = SuccessResponse(
                            data = {
                                "username": db_result[0],
                                "password": db_result[1],
                                "role": db_result[2]
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

    async def get_all_users() -> SuccessResponse | ErrorResponse:
        try:
            result = None
            query = '''
            SELECT username, password, role
            FROM api_users
            '''
            params = None
            async with mysql_pool.pool.acquire() as conn:
                await conn.select_db('auth_db')
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        query
                    )
                    db_result = await cursor.fetchall()
                    result = SuccessResponse(data=db_result)
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

    async def delete_user(
        username: str
    ) -> InfoResponse | ErrorResponse:
        try:
            result = None
            query = '''
            DELETE FROM api_users 
            WHERE username = %s
            '''
            params = (username,)
            async with mysql_pool.pool.acquire() as conn:
                await conn.select_db('auth_db')
                async with conn.cursor() as cursor:
                    result = await cursor.execute(
                        query,
                        params
                    )
                    await conn.commit()
                    if result > 0:
                        result = InfoResponse(message='APIUSER DELETED SUCCESSFULLY')
                        return result
                    else:
                        result = InfoResponse(message='APIUSER NOT FOUND')
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