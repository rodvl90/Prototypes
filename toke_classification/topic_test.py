from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
from pprint import pprint
# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
# nlp = pipeline("ner", model=model, tokenizer=tokenizer)

topic_tokenizer = AutoTokenizer.from_pretrained("andi611/distilbert-base-uncased-ner-agnews")

topic_model = AutoModelForSequenceClassification.from_pretrained("andi611/distilbert-base-uncased-ner-agnews")
topic_nlp = pipeline("sentiment-analysis", model=topic_model, tokenizer=topic_tokenizer)

text = "My name is Vlad Diac, and i, together with Mihai Birsan, founded Nimble Nexus in 2020. The birthplace of the company is in Romania, but we are currently based in the UK."

pprint(topic_nlp(text))

# pprint(gather_entities(nlp(text)))