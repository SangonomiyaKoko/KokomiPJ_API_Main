# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import API_Secruity, API_Auth
from . import SuccessResponse, ErrorResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_user(username: str):
    result: SuccessResponse | ErrorResponse = await API_Auth.get_user(
        username = username
    )
    return result.to_dict()
    
def check_permission(
    access_roles: list,
    token: str = Depends(oauth2_scheme)
):
    try:
        username,role = API_Secruity().decode_token(token=token)
        if username is None or role is None:
            raise HTTPException(
                status_code=401, 
                detail='Unauthorized'
            )
        userdata = {
            "username": username, 
            "role": role
        }
    except:
        raise HTTPException(
            status_code=401, 
            detail='Unauthorized'
        )
    for role in access_roles:
        if role in userdata['role']:
            return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail='Forbidden'
    )

class Permission:
    def check_root_permission(
        token: str = Depends(oauth2_scheme)
    ):
        return check_permission(
            access_roles=['root'],
            token=token
        )
