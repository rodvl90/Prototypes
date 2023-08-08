import asyncio
import json
import os
import sys
from pprint import pprint
from typing import Dict, List, Optional, Tuple

import aioredis as redis
import async_timeout
import httpx

# from data_parser import DataParserToolManager
from pydantic import BaseModel

import openai
from fastapi import FastAPI, HTTPException, Query, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

api_key = "..."
openai.api_key = api_key
class Message(BaseModel):
    role: str
    content: str
# data_parser_tool_manager = DataParserToolManager(openaikey=openai.api_key)
class OpenaiChatMessage(BaseModel):
    role: str
    content: str

class OpenaiChatMessagesRequest(BaseModel):
    stream: bool = False
    messages: List[OpenaiChatMessage]
# Parameters for OpenAI
openai_model = "gpt-3.5-turbo"
max_responses = 1
temperature = 0.7
max_tokens = 512

# Defining the FastAPI app and metadata
app = FastAPI(
    title="Streaming API",
    description="""### API specifications\n
To test out the Streaming API `chat`
              """,
    version=1.0,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Assuming your Svelte app runs on this host and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "CONNECT", "TRACE", "WebSocket"],
    allow_headers=["*"],
)
# Defining error in case of 503 from OpenAI
error503 = "OpenAI server is busy, try again later"

@app.post("/testRedis",tags=["testRedis"])
async def testRedis():
    r = await redis.from_url("redis://localhost:6379", password="i$fgfk^ga&lk*")
    await r.set("test", "test")
    response = await r.get("test")
    print(response)
    return response

@app.post("/chat",tags=["chat"])
async def chat(request: OpenaiChatMessagesRequest):
    data = request.dict()
    print("Data:\n",data,"\n\n")    
    stream = False
    if "stream" in data and data["stream"] == True:
        stream = True
    response_gen = chat_completion_post(data["messages"], stream)
    print("Chat stream: ",stream,"\n\n")
    response = [i async for i in response_gen]
    print("Chat response: ",response,"\n\n")
    if stream:
        return StreamingResponse(response_gen, media_type="application/json")
    else:
        output = jsonable_encoder({"role": "assistant", "content": response[0]})
        return JSONResponse(content=output)

async def openai_lib(messages,stream = False):
    print("OpenAI lib stream: ",stream,"\n\n")
    print("OpenAI lib messages: ",messages,"\n\n")
    return openai.ChatCompletion.create(
        model=openai_model,
        messages=messages,
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stream=stream
    )
async def chat_completion_lib(messages, stream=False):
    history = messages
    response = await openai_lib(history,stream)
    try:
        if stream:
            for chunk in response:
                current_content = chunk["choices"][0]["delta"]
                yield current_content
        else:
            current_content = response["choices"][0]["message"]["content"]
            yield current_content
    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))

async def chat_completion_post(messages:List[Message], stream:bool=False, nb_retries:int=3, delay:int=60) -> Optional[str]:
    
    """
    Sends a request to the ChatGPT API to retrieve a response based on a list of previous messages.
    """
    OPENAI_API_KEY = api_key
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    try:
        async with async_timeout.timeout(delay=delay):
            async with httpx.AsyncClient(headers=header) as aio_client:
                counter = 0
                keep_loop = True
                print(messages)
                while keep_loop:
                    try:
                        data = {
                                "model": "gpt-3.5-turbo",
                                "messages": messages,
                                "temperature":0.5,
                                "max_tokens": 256,
                                "top_p": 1,
                                "stream":stream,
                                "frequency_penalty": 0,
                                "presence_penalty": 0
                            }
                        async with aio_client.stream("POST",url = "https://api.openai.com/v1/chat/completions",json = data, timeout=30) as resp:
                            async for chunk in resp.aiter_bytes():
                                chunk_str = chunk.decode("utf-8")[len("data: "):]
                                # logger.debug(f"Chunk string : {chunk_str.strip()}")
                                 # Split the chunk string on newline characters
                                lines = chunk_str.strip().split("\n")
                                pprint(lines)
                                # Attempt to parse each line as JSON
                                for line in lines:
                                    if line:  # Avoid empty lines
                                            # Parse the JSON string to a dictionary
                                            chunk_dict = json.loads(line)
                                            pprint(chunk_dict)
                                            # Extract the content field
                                            content = chunk_dict.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                            print("Content: ",content,"\n\n")
                                            yield content
                    except httpx.ReadTimeout as e:
                        # logger.error(f"ReadTimeout occurred: {e}")
                        counter = counter + 1
                        keep_loop = counter < nb_retries
                    except Exception as e:
                        # logger.error("---------------------")
                        # logger.error(f"Exception occurred: {e}")
                        # logger.error(f"Exception type: {type(e)}")
                        # logger.error(f"Traceback: {traceback.format_exc()}")
                        # logger.error("---------------------")
                        counter = counter + 1
                        keep_loop = counter < nb_retries
    except asyncio.TimeoutError as e:
        print(f"Timeout {delay} seconds !")
    yield None
