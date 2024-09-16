from fastapi import FastAPI
from typing import Dict,List
import uvicorn

app = FastAPI()

@app.get("/")
async def home():
    return {"user_id": 1002}


@app.get("/shop")
async def shop():
    return {"shop": "商品信息"}


if __name__ == '__main__':
    #注意，run的第一个参数 必须是文件名:应用程序名
    uvicorn.run("quickstart:app", port=8080,  reload=True)
