# -*- coding: utf-8 -*-

import gc
import traceback

from .. import API_Logging
from .. import SuccessResponse, InfoResponse, ErrorResponse, BaseError
from ....model.users.user_basic import User, User_Basic, User_Basic_DB

class APP_User_Basic:
    async def get_user_counts():
        '''
        获取表中APP用户的总数量
        '''
        try:
            result = None
            parameter = []
            result: SuccessResponse | ErrorResponse = await User_Basic_DB().get_user_number()
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

    async def get_user_data_by_aid(
        aid: str,
        region: str
    ):
        '''
        获取指定用户的数据
        '''
        try:
            result = None
            parameter = []
            result: SuccessResponse | InfoResponse = await User_Basic_DB().get_user_data_by_aid(
                account_id=aid,
                region=region
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

    async def del_user_data_by_aid():
        ...