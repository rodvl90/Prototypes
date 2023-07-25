from transformers import BertTokenizer, DistilBertTokenizer, GPT2Tokenizer
from transformers import BertForSequenceClassification, DistilBertForSequenceClassification, GPT2LMHeadModel

class ModelHandler:
    def __init__(self, model_info):
        self.tokenizer_classes = {
            'bert': BertTokenizer,
            'distilbert': DistilBertTokenizer,
            'gpt2': GPT2Tokenizer
        }
        self.model_classes = {
            'bert': BertForSequenceClassification,
            'distilbert': DistilBertForSequenceClassification,
            'gpt2': GPT2LMHeadModel  # example for a GPT-2 language model
        }
        self.models = {}
        for name, model_type in model_info.items():
            self.models[name] = {
                'tokenizer': None,
                'model': None,
                'is_loaded': False,
                'model_type': model_type
            }
            
    def load_model(self, name, model_path, tokenizer_path):
        if name in self.models:
            tokenizer_class = self.tokenizer_classes.get(self.models[name]['model_type'])
            model_class = self.model_classes.get(self.models[name]['model_type'])
            if tokenizer_class is None or model_class is None:
                print(f"Invalid model type {self.models[name]['model_type']} for model {name}")
                return
            tokenizer = tokenizer_class.from_pretrained(tokenizer_path)
            model = model_class.from_pretrained(model_path)
            self.models[name]['tokenizer'] = tokenizer
            self.models[name]['model'] = model
            self.models[name]['is_loaded'] = True
        else:
            print(f"No model named {name} in handler")
            
    def use_model(self, name, text):
        if name in self.models and self.models[name]['is_loaded']:
            inputs = self.models[name]['tokenizer'](text, return_tensors="pt")
            outputs = self.models[name]['model'](**inputs)
            # ... rest of your model usage code here
        else:
            print(f"Model {name} is not loaded or does not exist")

# Usage:
handler = ModelHandler({'model1': 'bert', 'model2': 'distilbert'})
handler.load_model('model1', 'model1_path', 'tokenizer1_path')
handler.use_model('model1', 'some text')
handler.load_model('model2', 'model2_path', 'tokenizer2_path')
handler.use_model('model2', 'some other text')
