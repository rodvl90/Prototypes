from pprint import pprint

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# # Check if GPU is available and if not, fallback to CPU
# # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("philschmid/bart-large-cnn-samsum")
model = AutoModelForSeq2SeqLM.from_pretrained("philschmid/bart-large-cnn-samsum")
pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)
# Move model to the device
# model.to(device)
# def summarize(text):
#     # get input token length
#     token_length = len(tokenizer.encode(text))
#     # if token length is greater than 56, then use the pipeline
#     if token_length > 56:
#         return pipeline(text, max_length=  - 2)

def summarize(text):
    # Tokenize the input with specific max length and return as PyTorch tensors
    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    max_length = len(inputs[0]) / 2
    if max_length < 56:
        max_length = 56
    # Generate summary with the model
    summary_ids = model.generate(inputs, max_length=100, length_penalty=4.0, num_beams=4, early_stopping=True)

    # Decode the summary and return the result
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
def get_conversation(messages):
    result = []
    for message in messages:
        result.append(f"{message.get('role')}:{message.get('content')}")
    return "\n".join(result)
def chat_completion(messages):
    print("Messages:",messages)
    conversation = f"""
    {get_conversation(messages)}
    """
    print("Conversation:",conversation)
    print("Summary:",summarize(conversation))

    
text = """
User: Hi. My name is Vlad!
Chatbot: Hello Vlad, how are you?
User: I am fine, thank you. How are you?
Chatbot: I am fine, thank you. How can I help you today?
User: I would like to book a flight to London.
Chatbot: What is your departure location?
User: Bucharest.
Chatbot: What is your destination location?
User: London.
Chatbot: What is your departure date?
User: 12th of August.
Chatbot: What is your return date?
User: 19th of August.
Chatbot: How many passengers?
User: 2 adults and 1 child.
Chatbot: What is your budget?
User: 500 euros.
"""
messages = [{"role": "user","content": "Hello! My name is Vlad."},{"role": "chatbot","content": "Hi! How are you?"},{"role": "user","content": "I'm fine, thank you. I want to improve my notes."},{"role": "chatbot","content": "Sure. What would you want to improve exactly?"}]
chat_completion(messages)
