import aiomysql
import traceback
from . import mysql_pool, API_Logging

class API_Auth:
    async def add_user(username: str, password: str, roles: str):
        try:
            result = {
                'status': 'ok',
                'message': 'SUCCESS',
                'data': {}
            }
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
            result['message'] = 'APIUSER ADDED SUCCESSFULLY'
            return result
        except aiomysql.MySQLError as e:
            if e.args[0] == 1062:
                result['message'] = 'APIUSER ALREADY EXISTS'
                return result
            else:
                track_id = API_Logging().write_mysql_error(
                    error_file=__file__,
                    error_query=query,
                    error_data=str(params),
                    error_name=str(e)
                )
                result['status'] = 'error'
                result['message'] = 'MYSQL ERROR'
                result['data'] = {
                    'error_info': str(type(e).__name__),
                    'track_id': track_id
                }
                return result
        
    async def get_all_users():
        try:
            result = {
                'status': 'ok',
                'message': 'SUCCESS',
                'data': {}
            }
            query = '''
            SELECT id, username, role, created_at 
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
                    result['data'] = db_result
                    return result 
        except aiomysql.MySQLError as e:
            track_id = API_Logging().write_mysql_error(
                error_file=__file__,
                error_query=query,
                error_data=str(params),
                error_name=str(e)
            )
            result['status'] = 'error'
            result['message'] = 'MYSQL ERROR'
            result['data'] = {
                'error_info': str(type(e).__name__),
                'track_id': track_id
            }
            return result

    async def delete_user(username: str):
        try:
            result = {
                'status': 'ok',
                'message': 'SUCCESS',
                'data': {}
            }
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
                        result['message'] = 'APIUSER DELETED SUCCESSFULLY'
                        return result
                    else:
                        result['message'] = 'APIUSER NOT FOUND'
                        return result
        except aiomysql.MySQLError as e:
            track_id = API_Logging().write_mysql_error(
                error_file=__file__,
                error_query=query,
                error_data=str(params),
                error_name=str(e)
            )
            result['status'] = 'error'
            result['message'] = 'MYSQL ERROR'
            result['data'] = {
                'error_info': str(type(e).__name__),
                'track_id': track_id
            }
            return result