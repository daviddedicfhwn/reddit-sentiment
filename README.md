# Reddit Sentiment - Web Data Acquisition Project

This project is all about [reddit.com](https://reddit.com). Designed to gather data from popular subreddits and perform sentiment analysis on the collected data. The goal is to gain insights into the opinions and emotions of Reddit users and subreddits.

The scraper is implemented in Python, utilizing the Selenium library for web scraping and the [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) sentiment analysis model. The scraped data is stored in a MongoDB database, allowing for easy retrieval and analysis.

This project was created as part of the educational program for the BSc in Data Science at the [University of Applied Sciences Northwestern Switzerland](https://www.fhnw.ch/en/) (FHNW). The project was developed during the Web Datenbeschaffung (Web Data Acquisition) module, which focuses on accessing and extracting relevant information from the vast data sources available on the web.

## Usage

### Running locally

If running the project locally, you will need to install the required dependencies. This can be done by running the following command in the root directory of the project:

```bash
pip install -r requirements.txt
```

The required web driver for Selenium is included in the project. As a default, the scraper will use the Firefox web driver when running locally

In order to run the MongoDB needed to store the scraped data, you will need to have Docker installed. Once Docker is installed, you can run the following command in the root directory of the project:

```bash
docker-compose up -d mongodb
```

Alternatively, you can run the MongoDB locally on your machine. In this case, you will need to change the `MONGO_URI` in the `config.py` file to point to your local MongoDB instance.

Once the MongoDB is up and running, you can start the scraper by running the following command in the root directory of the project:

```bash
python main.py
```

### Running in Docker

> **Note:**
> Running the project in Docker is not the recommended way of running the project because of the resource intensive nature of the project and limited testing.  

If you have Docker installed, you can run the project in a Docker container. To do so, you will need to build the Docker image. This can be done by running the following command in the root directory of the project:

```bash
docker compose up -d --build
```

This will build the Docker image and start the MongoDB and scraper containers. 

## Configuration

The scraper can be configured by changing the values in the `config.py` file. The following values can be changed:

### Database
- `MONGODB_URI`: The URI of the MongoDB instance to use. Defaults to `mongodb://localhost:27017/`
- `DATABASE_NAME`: The name of the MongoDB database to use. Defaults to `reddit_sentiment`
- `POSTS_COLLECTION`: The name of the MongoDB collection to store the posts in. Defaults to `posts`
- `COMMENTS_COLLECTION`: The name of the MongoDB collection to store the comments in. Defaults to `comments`

### Scraping
- `SCROLL_TIME`: The time in seconds the script scrolls down on the subreddit page until the extraction of posts and comments begins. The longer the time, the more posts and comments will be extracted. Defaults to `2`
- `SUBREDDIT_LIST`: A list of subreddits to scrape. Defaults to `['aww']`
- `SUBREDDIT_FILE`: The file path of a JSON file containing a list of subreddits to scrape. Defaults to `"./data/subreddits.json"`
- `MAX_POSTS_PER_SUBREDDIT`: The maximum number of posts to scrape per subreddit. Defaults to `None` (no limit)

### Sentiment analysis
- `SENTIMENT_ANALYSIS`: Whether to perform sentiment analysis on the scraped data. Defaults to `True`
- `SENTIMENT_FEATURES`: The feature to use for sentiment analysis. Consists of the MongoDB collection name and the field name. Defaults to `[(POSTS_COLLECTION, 'title'), (COMMENTS_COLLECTION, 'text')]`
- `SENTIMENT_MODEL`: The sentiment analysis model to use. Defaults to `"cardiffnlp/twitter-xlm-roberta-base-sentiment"`

### Selenium Driver
- `DRIVER_OPTIONS`: The options for the Firefox webdriver. Defaults to the options returned by the `get_driver_options()` function in the `config.py` file.

### Selenium Driver
The Selenium driver arguments are also defined in the `config.py` file. Per default the driver runs with the following arguments:
- `--headless`: Run the driver in headless mode
- `--no-sandbox`: Disable the sandbox mode

In addition to these arguments, the following preferences are set:
- `profile.managed_default_content_settings.images`: `2` (disable images)

## Docker stack

The project includes a Docker stack, which can be used to run the scraper and MongoDB in Docker containers. The stack consists of the following services:

- `mongodb`: The MongoDB database
- `scraper`: The scraper itself
- `selenium-hub`: The Selenium hub
- `firefox`: The Firefox Selenium node

## Scraping

The scraper will scrape the following data from the specified subreddits:
- Posts
  - Title
  - URL
  - Author
  - Post ID
  - Subreddit

- Comments
  - Text
  - Author
  - Upvotes
  - Parent Comment ID
  - Post ID
  - Subreddit

The scraped data is stored in a MongoDB database. The posts are stored in the `posts` collection and the comments are stored in the `comments` collection. 

## Sentiment analysis

The sentiment analysis is performed using the [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) model per default. The model is able to classify text into three classes: `positive`, `negative` and `neutral`. The label with the highest probability is chosen as the class for the text and stored in the `sentiment` field of the respective MongoDB document.

The model can be changed by changing the `SENTIMENT_MODEL` in the `config.py` file. The model can be any model from the [Hugging Face model hub](https://huggingface.co/models).

The analysis can be disabled by setting the `SENTIMENT_ANALYSIS` in the `config.py` file to `False`. In case you want to run the analysis only, you can start the scraper with the `--sentiment-only` flag:

```bash
python main.py --sentiment-only
```

## Tests

The project includes a number of unit and integration tests. These tests can be run by running the following command in the root directory of the project:

```bash
python -m unittest discover
```

Make sure a MongoDB instance is running before running the tests as the integration tests require a running MongoDB instance.

It is recommended to run the tests within PyCharm or any IDE providing a graphical test runner.