from fastapi import FastAPI
from fastapi.middleware import Middleware
from pydantic import BaseModel

from uvicorn_logger import AccessLoggerMiddleware

app = FastAPI(middleware=[Middleware(AccessLoggerMiddleware)])


@app.get("/")
async def home():
    ...


class Body(BaseModel):
    a: str


@app.post("/another")
async def another(body: Body):
    return body
