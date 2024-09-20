import gc
import traceback
from .. import API_Logging, API_Secruity, API_Auth
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

class API_Users:
    async def get_api_user(
    ):
        '''
        Get all API users in Mysql
        '''
        try:
            result = None
            parameter = []
            result: SuccessResponse | ErrorResponse = await API_Auth.get_all_users()
            return result.to_dict()
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameter,
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
            ).to_dict()
            return result
        finally:
            gc.collect()

    async def del_api_user(
        username: str
    ):
        '''
        Deleting API users from MySQL
        '''
        try:
            result = None
            parameter = [username]
            result: InfoResponse | ErrorResponse = await API_Auth.delete_user(
                username=username
            )
            return result.to_dict()
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameter,
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
            ).to_dict()
            return result
        finally:
            gc.collect()

    async def add_api_user(
        username: str,
        password: str,
        roles: str
    ):
        '''
        Adding API User to Mysql
        '''
        try:
            result = None
            parameter = [username,password,roles]
            hashed_password = API_Secruity().encode_password(password=password)
            result: InfoResponse | ErrorResponse = await API_Auth.add_user(
                username=username,
                password=hashed_password,
                roles=roles
            )
            return result.to_dict()
        except Exception as e:
            error_info = traceback.format_exc()
            track_id = API_Logging().write_api_error(
                error_file=__file__,
                error_params=parameter,
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
            ).to_dict()
            return result
        finally:
            gc.collect()