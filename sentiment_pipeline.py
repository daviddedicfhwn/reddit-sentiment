from transformers import pipeline
import asyncio

class SentimentPipeline:
    def __init__(self, pipeline_name="sentiment-analysis"):
        self.pipeline = pipeline(pipeline_name)

    def get_sentiments(self, data):
        if len(data) > 100):
            return self.get_sentiment_batches(data)
        sentiment =  self.pipeline(data)
        return sentiment, data
    
    def get_sentiment_batches(self, data):
        sentiments = []
        
    