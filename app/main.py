from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .common.dependencies import Permission, get_user
from .core.secruity import API_Secruity
from .api.root.urls import router as root_router
import uvicorn

app = FastAPI()

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
    user = get_user(form_data.username)
    _API_Secruity = API_Secruity()
    if not user or not _API_Secruity.verify_password(
        plain_password=form_data.password, 
        hashed_password=user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = _API_Secruity.create_access_token(
        data = {
            "sub": user["username"], 
            "role": user["role"]
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
        host='127.0.0.1',
        port=8080
    )
