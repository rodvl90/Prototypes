import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
history = [{"role": "system", "content": "you are a helpful ai!"},{"role": "user", "content": "Hi!My name is vlad!"}]
# history.extend(messages)
# res = "test"
res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=history,
    temperature=0.5,
    max_tokens=50,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
)
print(res)