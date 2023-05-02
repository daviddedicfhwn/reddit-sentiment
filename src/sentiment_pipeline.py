from transformers import pipeline
import torch.nn.functional as F
import torch

class SentimentPipeline:
    
    def __init__(self, window_size=512, stride=256):
        self.pipeline = pipeline('sentiment-analysis')
        self.window_size = window_size
        self.stride = stride

    def get_sentiments(self, data):
        if len(data) > 100:
            return self.get_sentiment_batches(data)
        sentiment =  self.pipeline(data)
        return sentiment, data
    
    def get_sentiment_batches(self, data):
        sentiments = []

    def get_tokenized_sentiment(self, data):
        # tokenize the input text
        tokens = self.pipeline.tokenizer(data, truncation=True, padding=True, max_length=self.window_size)

        # split the input into sub-segments of size window_size with stride stride
        input_ids_list = []
        attention_mask_list = []
        for i in range(0, len(tokens['input_ids']), self.stride):
            window_tokens = {k: v[i:i+self.window_size] for k, v in tokens.items()}
            input_ids = torch.tensor(window_tokens['input_ids'])
            attention_mask = torch.tensor(window_tokens['attention_mask'])
            input_ids_list.append(input_ids)
            attention_mask_list.append(attention_mask)

        # process each sub-segment separately
        results = []
        for input_ids, attention_mask in zip(input_ids_list, attention_mask_list):
            # pad the input_ids tensor to always have a second dimension of window_size
            padding_length = self.window_size - input_ids.shape[0]
            input_ids = F.pad(input_ids, (0, padding_length), 'constant', self.pipeline.tokenizer.pad_token_id)
            attention_mask = F.pad(attention_mask, (0, padding_length), 'constant', 0)

            # pass the encoded input through the sentiment-analysis model
            result = self.pipeline.model(input_ids=input_ids.unsqueeze(0), attention_mask=attention_mask.unsqueeze(0))

            # print the result of the sentiment-analysis model and say if the score is positive or negative
            label = 'POSITIVE' if result[0][0][0] > result[0][0][1] else 'NEGATIVE'
            score = torch.softmax(result[0], dim=1).max().item()
            results.append((label, score))

        # aggregate the results to get the overall sentiment
        positive_scores = [score for label, score in results if label == 'POSITIVE']
        negative_scores = [score for label, score in results if label == 'NEGATIVE']
        if len(positive_scores) > len(negative_scores):
            label = 'POSITIVE'
            score = sum(positive_scores) / len(positive_scores)
        elif len(negative_scores) > len(positive_scores):
            label = 'NEGATIVE'
            score = sum(negative_scores) / len(negative_scores)
        else:
            label = 'NEUTRAL'
            score = 0.5

        return { 'label': label, 'score': score }