from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import hashlib
from datetime import datetime, timedelta, timezone
import uvicorn

app = FastAPI()

# 秘钥和算法
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 使用 OAuth2PasswordBearer 进行身份验证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# 模拟的用户数据库（实际应使用 MySQL 等数据库）
users_db = {
    "root": {
        "username": "root",
        "password": hashlib.sha256("password".encode()).hexdigest(),
        "role": "['root']",
    },
    "root": {
        "username": "root",
        "password": hashlib.sha256("rootpassword".encode()).hexdigest(),
        "role": "['bot']",
    }
}

# 创建访问令牌
def create_access_token(data: dict):
    to_encode = data.copy()
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 校验密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

# 获取用户数据
def get_user_by_username(username: str):
    return users_db.get(username)

# 登录接口，获取 JWT 令牌
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户信息，校验令牌和权限
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 示例接口：只能由 root 角色访问
@app.get("/root-only")
async def root_only(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "root":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"message": "Welcome, root user!"}

if __name__ == '__main__':
    #注意，run的第一个参数 必须是文件名:应用程序名
    uvicorn.run(app, host='127.0.0.1', port=8080)