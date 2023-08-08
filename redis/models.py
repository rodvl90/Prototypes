from typing import Dict, List

from fastapi import UploadFile
from pydantic import BaseModel


class Config(BaseModel):
    openai_key: str
    system_prompt: str
    
class ConfigUpdate(BaseModel):
    session_id: str
    config: dict

class Query(BaseModel):
    query: str
    top_k: int
    
class Session(BaseModel):
    session_id: str
 
class FileUpload(BaseModel):
    file: UploadFile

class FileData(BaseModel):
    path: str
    metadata: dict

class OpenaiChatMessage(BaseModel):
    role: str
    content: str

class OpenaiChatMessages(BaseModel):
    messages: List[Dict[str, str]]

class OpenaiChatMessagesRequest(BaseModel):
    session_id: str
    messages: List[OpenaiChatMessage]