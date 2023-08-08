import json
import uuid
from pprint import pprint

import aioredis as redis
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import Config, ConfigUpdate, FileUpload, OpenaiChatMessagesRequest, Query
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

r = redis.from_url('redis://localhost:6379')

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response

app = FastAPI(
    title="Foundation",
    description="An API for building intelligent assitants.",
    version="0.1.0",
    middleware=[Middleware(LoggingMiddleware)],
)

@app.post("/get_session", tags=["System"])
async def get_configuration(session_id : str = Form(...)):
    
    config = await get_config(r,session_id)
    return {"config": config}
@app.post("/auth", tags=["System"])
async def create(config: Config):
    
    session_id = await create_session(r,config.dict())
    return {"session_id": session_id}

@app.post("/update_config", tags=["System"])
async def session_update( update_data: ConfigUpdate):
    session_id = update_data.session_id
    config = update_data.config
    
    response = await update_config(r,session_id, config)
    return {"data": response}

async def get_config(redis, session_id):
    config = await redis.get(session_id)
    config = json.loads(config)
    return config

async def update_config(redis, session_id, updated_config):
        config = await redis.get(session_id)
        output = {"old": json.loads(config)}
        config = json.loads(config)
        config.update(updated_config)
        output["new"] = config
        await redis.set(session_id, json.dumps(config))
        return output

async def create_session(redis, config):
    print(config)
    session_id = _generate_session_id()

    await redis.set(session_id, json.dumps(config))
    
    return session_id 

def _generate_session_id():
    return str(uuid.uuid4())