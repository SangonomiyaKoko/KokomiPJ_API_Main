# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import API_Secruity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

fake_users_db = {
    "root": {
        "username": "root",
        "password": "9a3d1cc750db369112832a05ab5d32e54d4905c76e565eb9ca005947dce8ce95",
        "role": "['root']"
    }
}


def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return user_dict
    
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
