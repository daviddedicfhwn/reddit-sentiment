import re

import numpy as np
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig

from src.config import COMMENTS_COLLECTION, SENTIMENT_MODEL, POSTS_COLLECTION


class SentimentPipeline:
    """
    A Sentiment Pipeline class that provides methods to interact with the huggingface sentiment model.
    """

    def __init__(self, model_path=SENTIMENT_MODEL):
        """
        Initialize the Sentiment Pipeline class.

        :param model_path: The huggingface model path. Defaults to the path specified in the config.
        """
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.config = AutoConfig.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)

    def get_tokenized_sentiment(self, data, collection=COMMENTS_COLLECTION):
        """
        Get the sentiment of the input data.

        :param data: Your input string
        :param collection: The collection type of the input data. Defaults to COMMENTS_COLLECTION which is specified in the config.
        :return: A dictionary containing the sentiment label and score.
        """

        # anonymize the input text
        text = self.preprocess(data, type=collection)

        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)

        # get the sentiment label and convert the score to a probability
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)[::-1]

        return {
            'label': self.config.id2label[ranking[0]],
            'score': np.round(float(scores[ranking[0]]), 4)
        }

    def preprocess(self, text, type):
        """
        Preprocesses/Anonymizes the input text. Removes URLs, subreddit names and usernames.

        :param type: The collection to which the sentiment belongs to.
        :return: The preprocessed text without URLs, subreddit names or usernames.
        """
        patterns = [
            (r'u\/[\w\d\-_]+', 'user'),
            (r'r\/[\w\d\-_]+', 'subreddit'),
            (r'\bhttps?:\/\/[^\s]+\b', 'link')
        ]

        if type == POSTS_COLLECTION:
            text.replace("_", " ")

        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)

        return text
