# -*- coding: utf-8 -*-

'''
Separate modules for each platform, and their interfaces are defined in these modules
'''

from ..services.user_service import API_Auth
from ..core.secruity import API_Secruity
from ..log.log import API_Logging
from ..schemas.responses import SuccessResponse, InfoResponse, ErrorResponse, BaseError