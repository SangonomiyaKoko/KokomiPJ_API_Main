# -*- coding: utf-8 -*-

'''
The business logic layer is responsible for implementing the business processing behind the API
'''

from ..db.mysql import mysql_pool
from ..db.redis import redis_pool
from ..common.logging import API_Logging
from ..schemas.responses import SuccessResponse, InfoResponse, ErrorResponse, BaseError, BaseResponse