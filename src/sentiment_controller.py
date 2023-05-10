import logging

from src.database import MongoDBClient
from src.sentiment_pipeline import SentimentPipeline

logger = logging.getLogger(__name__)


class SentimentController:
    def __init__(self):
        self.sentiment_pipeline = SentimentPipeline()

    def write_sentiments_to_documents(self, collection, field_to_analyze):
        with MongoDBClient() as db_client:
            for document in db_client.db[collection].find():
                # get sentiment for current document
                sentiment = self.sentiment_pipeline.get_tokenized_sentiment(data=document[field_to_analyze],
                                                                            collection=collection)
                # update current document with sentiment
                db_client.update_data_by_id(collection, document['_id'], {'sentiment': sentiment})

                logger.info(
                    f'Updated {document["_id"]} with Senitment Score {sentiment["score"]} and Sentiment Label {sentiment["label"]}.')
