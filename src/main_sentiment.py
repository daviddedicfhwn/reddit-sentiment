import database
import config
from sentiment_pipeline import SentimentPipeline

database.connect_to_db()

db_client = database.db
sentiment_pipeline = SentimentPipeline()

for doc in db_client[config.COMMENTS_COLLECTION].find().limit(10):
    # get sentiment for current doc
    #sentiment = sentiment_pipeline.get_sentiments(data = doc['text'])
    #print(len(doc['text']), sentiment)
    # update each doc with sentiment
    #database.update_data_by_id(config.COMMENTS_COLLECTION, doc['_id'], {'sentiment': sentiment['label']})
    #print('updated:', doc['_id'], 'with text', doc['text'], 'and sentiment', sentiment['label'])
    
    print(doc['text'], sentiment_pipeline.get_tokenized_sentiment(doc['text']))