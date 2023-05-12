"""
Fetch the display names of popular subreddits and save them to a JSON file.

Usage:
    python scripts/fetch_subreddits.py

    Add your Reddit API credentials to a .env file in the same directory as this script.
"""


import json
import os

import praw
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_popular_subreddits(limit=50):
    """
    Get the display names of popular subreddits.

    :param limit: The number of subreddits to fetch (default is 100).
    :return: A list of display names of popular subreddits.
    """
    # Authenticate with Reddit API using environment variables
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent=os.getenv("REDDIT_USER_AGENT"))


    # Get popular subreddits
    subreddits = reddit.subreddits.popular(limit=limit, params={"t": "all"})
    # Store the subreddits' display_name in a list
    subreddit_list = [subreddit.display_name for subreddit in subreddits]

    return subreddit_list


def save_subreddits_to_json(subreddit_list, filename=os.getenv("SUBREDDITS_FILENAME", "../data/subreddits.json")):
    """
    Save a list of subreddit display names to a JSON file.

    :param subreddit_list: A list of subreddit display names.
    :param filename: The name of the JSON file to save the subreddits (default is "subreddits.json").
    """
    # Save the list of subreddits to a JSON file
    with open(filename, "w") as file:
        json.dump(subreddit_list, file, indent=4)


if __name__ == "__main__":
    popular_subreddits = get_popular_subreddits()
    save_subreddits_to_json(popular_subreddits)
