# from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
# from transformers import pipeline


# model = AutoModel.from_pretrained("../../models/distilbert-base-uncased-ner-agnews")

# tokenizer = AutoTokenizer.from_pretrained("../../models/distilbert-base-uncased-ner-agnews", device_map="auto")

# # model = AutoModelForSequenceClassification.from_pretrained("../../models/distilbert-base-uncased-ner-agnews")

# text = "My name is Vlad Diac, and i, together with Mihai Birsan, founded Nimble Nexus in 2020. The birthplace of the company is in Romania, but we are currently based in the UK."
text = "What a beautiful view! I love this place."

# topic_nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# print(topic_nlp(text))
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

tokenizer = DistilBertTokenizer.from_pretrained('../../models/distilbert-base-uncased-ner-agnews')
model = DistilBertForSequenceClassification.from_pretrained('../../models/distilbert-base-uncased-ner-agnews')

inputs = tokenizer(text, return_tensors="pt")
labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
outputs = model(**inputs, labels=labels)
loss = outputs.loss
logits = outputs.logits


# Get the predicted class index as before
probs = torch.nn.functional.softmax(logits, dim=-1)
predicted_class_index = torch.argmax(probs, dim=-1)

# Map the predicted class index to its corresponding label using the model's config
predicted_class_label = model.config.id2label[predicted_class_index.item()]

print(predicted_class_label)
