from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
import config
from scipy.special import softmax

class SentimentPipeline:
    
    def __init__(self, model_path="cardiffnlp/twitter-xlm-roberta-base-sentiment", window_size=512, stride=256):
        self.model_path = model_path
        self.window_size = window_size
        self.stride = stride
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.config = AutoConfig.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)

    def get_tokenized_sentiment(self, data, collection=config.COMMENTS_COLLECTION):
        text = self.preprocess(data, type=collection)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)[::-1]
        return { 
                'label': self.config.id2label[ranking[0]], 
                'score': np.round(float(scores[ranking[0]]), 4) 
               }
    
    def preprocess(self, text, type):
        if type == config.POSTS_COLLECTION:
            text.replace("_", " ")
            
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)