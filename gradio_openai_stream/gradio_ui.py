import json
from pprint import pprint

import gradio as gr
import requests

memory = []

def chat(lines):
    url = "http://127.0.0.1:8000/chat"
    headers = {"Content-Type": "application/json"}

    # Convert lines of text to list of dicts
    lines = [{"role": "user", "content": line} for line in lines.split("\n") if line]
    data = json.dumps(lines)
    memory.extend(lines)
    print("MEMORY:","-"*30)
    pprint(memory)
    response = requests.post(url, headers=headers, data=data)

    # Extract the messages from the response
    messages = response.json()
    
    # Combine all messages into a single string
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

iface = gr.Interface(fn=chat, inputs=gr.inputs.Textbox(lines=5, placeholder="Type something here..."), outputs=gr.outputs.Textbox())
iface.queue().launch()
