import gc
import traceback
from .. import API_Logging, API_Auth
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError

async def main(
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