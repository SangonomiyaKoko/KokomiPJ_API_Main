# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from .core.config import settings
from .common.dependencies import Permission, get_user
from .core.secruity import API_Secruity
from .db.mysql import mysql_pool
from .db.redis import redis_pool
from .api.root.urls import router as root_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await mysql_pool.init_pool()
        print('INFO:     Connection has been established with MySQL')
    except:
        print('ERROR:    Failed to establish connection with MySQL')
    try:
        await redis_pool.init_pool()
        print('INFO:     Connection has been established with Redis')
    except:
        print('ERROR:    Failed to establish connection with Redis')
    yield
    await mysql_pool.close_pool()
    print('INFO:     The connection to MySQL has been closed')
    await redis_pool.close_pool()
    print('INFO:     The connection to Redis has been closed')

app = FastAPI(lifespan=lifespan)

@app.get("/", summary='Root', tags=['Default'])
async def root():
    """
    Root router

    Parameters:
    - None

    Returns:
    - str

    """
    return {'status':'ok','messgae':'Hello! Welcome to Kokomi Interface.'}


@app.post("/token", summary='Login', tags=['Default'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if user['status'] != 'ok':
        raise HTTPException(status_code=500, detail="Internal Server Error")
    _API_Secruity = API_Secruity()
    if not user or not _API_Secruity.verify_password(
        plain_password=form_data.password, 
        hashed_password=user['data']["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = _API_Secruity.create_access_token(
        data = {
            "sub": user['data']["username"], 
            "role": user['data']["role"]
        }
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

app.include_router(
    root_router, 
    prefix="/root", 
    tags=['Root Interface'],
    dependencies=[Depends(Permission.check_root_permission)]
)

def main():
    uvicorn.run(
        app=app,
        host=settings.API_HOST,
        port=settings.API_PORT
    )
