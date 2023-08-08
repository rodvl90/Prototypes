# import tiktoken
import asyncio
import json
import uuid
from pprint import pprint
from time import sleep

import openai


class DataParserToolManager:
    def __init__(self,openaikey=None):
        openai.api_key = openaikey
        self.chat_model = "gpt-4"
        self.redis = None
        
    
    async def chat_completion(self,messages,stream=False):
        history = messages
        print("Chat completion stream: ",stream,"\n\n")
        response = openai.ChatCompletion.create(
            model=self.chat_model,
            messages=history,
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stream=stream
        )
        try:
            if stream:
                print("returning stream")
                for chunk in response:
                    current_content = chunk["choices"][0]["delta"].get("content", "")
                    yield current_content
            else:
                print("returning response")
                return response["choices"][0]["message"]
        except Exception as e:
            print("OpenAI Response (Streaming) Error: " + str(e))
            
    
   