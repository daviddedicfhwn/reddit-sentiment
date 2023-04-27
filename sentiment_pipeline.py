from transformers import pipeline

class SentimentPipeline:
    def __init__(self, pipeline_name="sentiment-analysis"):
        self.pipeline = pipeline(pipeline_name)

    def get_sentiments(self, data):
        sentiment =  self.pipeline(data)
        return sentiment, data

