import gc
import traceback
from .. import API_Logging, API_Auth

async def main(
):
    '''
    Get all API users in Mysql
    '''
    try:
        result = {
            'status': 'ok',
            'message': 'SUCCESS',
            'data': {}
        }
        parameter = []
        db_result = await API_Auth.get_all_users()
        if db_result['status'] == 'ok':
            result['message'] = db_result['message']
        else:
            return db_result
        return result
    except Exception as e:
        error_info = traceback.format_exc()
        track_id = API_Logging().write_api_error(
            error_file=__file__,
            error_params=parameter,
            error_name=str(type(e).__name__),
            error_info=error_info
        )
        result['status'] = 'error'
        result['message'] = 'PROGRAM ERROR'
        result['data'] = {
                'error_info': str(type(e).__name__),
                'track_id': track_id
            }
        return result
    finally:
        gc.collect()