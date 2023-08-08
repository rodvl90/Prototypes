from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
from pprint import pprint
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

topic_tokenizer = AutoTokenizer.from_pretrained("andi611/distilbert-base-uncased-ner-agnews")

topic_model = AutoModelForSequenceClassification.from_pretrained("andi611/distilbert-base-uncased-ner-agnews")
topic_nlp = pipeline("ner", model=topic_model, tokenizer=topic_tokenizer)
text = "I am a professionally qualified fire engineer with 7 years experience. I have recently achieved RTITB accreditation in the use of Counterbalance fork lift trucks and I am seeking employment that will make best use of my skills and allow me to develop them further."
query= "Give me the aplicants that have rtitb accreditation"
print(nlp(text),"\n\n",nlp(query))
def gather_entities(text):
    return nlp(text)

# def process_entities(nlp_output):
#     result = {}
#     for entry in nlp_output:
#         entity_type = entry['entity'].split('-')[-1]  # Get the entity type (PER, ORG, LOC, etc.)
#         word = entry['word']
        
#         # If it's a continuation of a word, remove the '##'
#         if word.startswith('##'):
#             word = word[2:]
        
#         # If we've seen this entity type before, append the word
#         if entity_type in result:
#             result[entity_type].append(word)
#         else:  # Else, start a new list with this word
#             result[entity_type] = [word]

#     # Join the split words together and remove any duplicates
#     for key in result:
#         result[key] = list(set([' '.join(word.split()) for word in result[key]]))

#     return result

def process_entities(entities):
    result = {}
    current_entity_group = None
    current_entity_words = []
    current_end_position = None

    for entity in entities:
        entity_type = entity['entity']
        entity_word = entity['word']
        start_position = entity['start']

        if entity_word.startswith('##'):
            # Remove '##' and append to the previous word
            entity_word = entity_word[2:]
            if start_position > current_end_position:
                entity_word = ' ' + entity_word
            current_entity_words[-1] += entity_word
        else:
            if current_entity_group is not None:
                # Save the previous entity group
                if current_entity_group in result:
                    result[current_entity_group].append(' '.join(current_entity_words))
                else:
                    result[current_entity_group] = [' '.join(current_entity_words)]

            # Check if a new entity is starting
            if entity_type.startswith('B-'):
                current_entity_group = entity_type[2:]  # Removing 'B-'
                current_entity_words = [entity_word]
            elif entity_type.startswith('I-') and entity_type[2:] == current_entity_group:
                # The same entity continues
                current_entity_words.append(entity_word)
        
        current_end_position = entity['end']

    # Save the last entity group
    if current_entity_group is not None:
        if current_entity_group in result:
            result[current_entity_group].append(' '.join(current_entity_words))
        else:
            result[current_entity_group] = [' '.join(current_entity_words)]
    
    return result



pprint(process_entities(nlp(text)))
pprint(process_entities(nlp(query)))