import config
from scraper import SubredditScraper

def main():
    subreddit_list = ['popular']
    scraper = SubredditScraper(config.DRIVER_OPTIONS)

    for subreddit in subreddit_list:
        scraper.scrape_subreddit(subreddit, sentiment=config.SENTIMENT_ANALYSIS)

if __name__ == '__main__':
    main()
