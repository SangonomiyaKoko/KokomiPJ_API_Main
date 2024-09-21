# -*- coding: utf-8 -*-

'''
Separate modules for each platform, and their interfaces are defined in these modules
'''

from ..schemas.responses import SuccessResponse, InfoResponse, ErrorResponse, BaseError
from ..services.user_service import API_Auth
from ..services.api_tracking import API_Tracker
from ..core.secruity import API_Secruity
from ..log.log import API_Logging
from ..db.mysql import mysql_pool
from ..db.redis import redis_pool