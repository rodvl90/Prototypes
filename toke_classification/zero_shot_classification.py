from pprint import pprint

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
pipeline1 = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# sequence_to_classify = "How do I get a certificate?"
sequence_to_classify = "Can you please elaborate?"
# sequence_to_classify = "Hello"
candidate_labels = ['data query', 'conversation history']
output = pipeline1(sequence_to_classify, candidate_labels)
pprint(output)

