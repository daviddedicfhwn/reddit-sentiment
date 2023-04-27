from sentiment_pipeline import SentimentPipeline

sentiment = SentimentPipeline().get_sentiments("I have no opinion")
print(sentiment)