from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

tokenizer = DistilBertTokenizer.from_pretrained('../../models/distilbert-base-uncased-ner-agnews')
model = DistilBertForSequenceClassification.from_pretrained('../../models/distilbert-base-uncased-ner-agnews')

# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

text = "My name is Vlad Diac, and i, together with Mihai Birsan, founded Nimble Nexus in 2020. The birthplace of the company is in Romania, but we are currently based in the UK."
# text = "What a beautiful view! I love this place."
k = 3  # Set your 'k' value

inputs = tokenizer(text, return_tensors="pt")
labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1

# Send inputs and labels to the device
inputs = {name: tensor.to(device) for name, tensor in inputs.items()}
labels = labels.to(device)

outputs = model(**inputs, labels=labels)
logits = outputs.logits

# Get the softmax probabilities and the predicted class indices for top-k predictions
probs = torch.nn.functional.softmax(logits, dim=-1)
top_k_probs, top_k_indices = torch.topk(probs, k)

# Convert top_k_indices tensor to a list
top_k_indices = top_k_indices.tolist()[0]

# Map the top-k indices to their corresponding labels using the model's config
top_k_labels = [model.config.id2label[index] for index in top_k_indices]

# Print the top-k probabilities and their respective labels
for label, prob in zip(top_k_labels, top_k_probs[0]):
    print(f"{label}: {prob.item()}")