# Report: Web Scraper for Subreddit Posts and Comments

## 1. Introduction and Motivation

With the advent of social media, the internet has become a vast repository of user-generated content, providing insights into various facets of human behavior, trends, and opinions. Reddit, one of the largest social media platforms, hosts discussions on a multitude of topics through its numerous communities called subreddits. This report presents a web scraper designed to extract data from these subreddits for further analysis. The motivation for this project stems from the need to facilitate comprehensive data analysis and interpretation of discussions on Reddit, which can be valuable for market research, sentiment analysis, and trend forecasting among other applications.

## 2. Description of the Idea

The core idea is to create an automated tool capable of scraping data from specific subreddits. The tool, implemented as a Python script, is designed to extract not only the main post information but also the comments associated with each post. Extracted data includes the post's URL, title, author, and comments, among other elements. The data is then stored in a database for further analysis.

## 3. Data Science Aspects & Further Analysis of Results

The scraper collects raw data from the Reddit platform, which could be used for several data science applications, such as Natural Language Processing (NLP) tasks (e.g., sentiment analysis, topic modeling), trend analysis, or to study user behavior and interactions on social media platforms. 

After data collection, further analysis could involve preprocessing the text data (cleaning, tokenization, stemming/lemmatization, etc.), followed by exploratory data analysis to understand patterns, trends, or anomalies in the data. Advanced statistical and machine learning models could then be applied to derive deeper insights.

The `sentiment_analysis.ipynb` notebook provides a more comprehensive  analysis of Reddit posts and comments. Let's break down each section and provide some additional analysis:

1. **Data Import**: The data is imported from two CSV files – `posts_sentiment.csv` and `comments_sentiment.csv`. The `pandas` library is used to read the CSV files into DataFrame objects. 

2. **Data Examination**: The data is grouped by subreddit to see the distribution of the posts and comments across various subreddits. The subreddit 'worldnewsvideo' was found to have insufficient data and was thus removed from the analysis. 

3. **Null Value Check**: The dataframes are checked for null values. For posts, there seems to be no null values. However, comments data has some null values, specifically in the 'text' field. 

4. **Handling Missing Values**: A significant number of null comments are from the user 'AutoModerator', which is a bot. Since the analysis aims to focus on user-generated content, these bot-generated comments are removed. The remaining null comments are also investigated, and the decision is made to remove them since they don't contain any meaningful text.

5. **Sentiment Analysis**: The sentiment scores of the posts and comments are analyzed. A box plot is created to visualize the sentiment score distribution across different sentiment labels. The distribution seems to be fairly even for negative and positive sentiments, while neutral sentiments appear slightly less certain.

6. **Correlation of Post and Comment Sentiments**: A hypothesis is tested that the sentiment of a post is correlated with the sentiment of its comments. Various visualizations and a correlation matrix are used to test this hypothesis. However, the results don't show a clear correlation.

7. **Subreddit Sentiment Analysis**: The sentiments of different subreddits are analyzed. It's found that the subreddit 'movies' has the most negative posts, 'wallstreetbets' has the most neutral ones, and 'damnthatsinteresting' has the most positive posts. 

8. **User Sentiment Analysis**: The sentiment scores are also analyzed by the author of the comments. It might be interesting to check if there are users who consistently post more positive or negative comments.

9. **Correlation between Comment Upvotes and Sentiment**: Lastly, the relationship between the number of upvotes a comment receives and its sentiment is explored. However, no clear correlation is found.

## 4. Relevancy to Real World

The scraper provides a robust way to collect data from Reddit, a platform that hosts a broad range of discussions on various topics. This makes the tool highly relevant in several domains:

- **Market Research:** Businesses can use the data to understand user sentiment towards their brand or products, identify emerging trends, or analyze competitors.
- **Academic Research:** Researchers in fields like sociology, psychology, or linguistics can study online behavior, language use, and cultural trends.
- **Public Opinion:** The data can provide insights into public opinion on various social, political, or economic issues.

## 5. Originality

The idea of scraping data from Reddit subreddits, while not entirely new, carries its own originality in the context of data analysis and research. Reddit is a vast platform with diverse content, and the concept of extracting and analyzing this data presents a unique opportunity for various applications.

The originality lies in the specific approach taken in this project. The focus is not just on scraping posts, but also on extracting all associated comments, providing a more comprehensive view of the discussions happening on the platform. This approach allows for a deeper understanding of user interactions, sentiments, and trends, which can be valuable in fields like market research, sentiment analysis, and social studies.

Moreover, the robustness of the scraper, its ability to handle exceptions, and its focus on specific subreddits add to the uniqueness of the project. These features make the tool more reliable and tailored to specific research needs, setting it apart from more generic scraping tools.

## 6. Usefulness

The script provides a convenient, automated way to collect large amounts of data from Reddit. The structured data it collects can be used directly for data analysis, saving researchers considerable time and effort compared to manual data collection. Its robust error handling also ensures the scraping process can run unattended, making it a reliable tool for large-scale data collection.


## 7. Technical Aspects and Implementation

The `SubredditScraper` class, implemented using Selenium, automates the process of data extraction from specific Reddit subreddits.

The scraping process begins by loading the target subreddit page using Selenium's `driver.get()` function. The URL for the subreddit is generated by the `get_subreddit_url()` method.

XPath, a language for navigating through HTML elements, is used extensively to access desired data on the page. For instance, the `extract_post_data()` method uses XPath to locate post containers on the webpage and extract the hyperlinks of each post.

The `extract_author()` method employs XPath to access the author of a post, identified by a specific class name 'author-name'. 

Comments from each post are extracted using the `extract_comments_data()` and `process_comments()` methods. XPath is used to locate all non-deleted comments, and each comment is processed individually to extract details such as the author, score (upvotes), and the subreddit.

The scraper handles exceptions like `NoSuchElementException` and `TimeoutException` by logging the error and moving on to the next post or comment, ensuring uninterrupted scraping operation.

The `WebDriverWait().until(EC.url_matches())` function, which uses regular expressions, ensures that the scraper waits until the URL matches the target subreddit before proceeding with the scraping. 

In summary, the Reddit Scraper effectively utilizes HTML, XPath, and regex to access and extract desired data from Reddit.


## 8. Conclusion

In conclusion, the script provides a robust, efficient, and convenient way to collect data from Reddit for various data analysis applications. Its ability to extract comprehensive data from specific subreddits and its robust exception handling make it a robust project. In the data report (jupyter notebook) we tried to analyze the data in a deeper way, trying to find correlations between sentiments of posts and their comments - but we couldn't find a more conclusive description to our data.