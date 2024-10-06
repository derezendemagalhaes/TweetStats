import os
import time
import tweepy
import datetime
import json
import logging

from dotenv import load_dotenv
from typing import Any, Dict, List
from requests.exceptions import Timeout

logging.basicConfig(level=logging.INFO)


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load tweet data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing tweet data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a tweet.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def get_tweets(days=7, max_retries=3, delay=5):
    """Retrieve tweets from the last days containing the hashtag #FlixBus with retries."""
    load_dotenv()
    
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, timeout=10)  # Add timeout for requests

    since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    until_date = datetime.datetime.now().strftime("%Y-%m-%d")

    hashtag = "#flixbus"
    tweets_data = []

    for attempt in range(max_retries):
        try:
            tweets = tweepy.Cursor(api.search_tweets, q=hashtag, since=since_date, until=until_date, lang='en').items()
            for tweet in tweets:
                tweets_data.append(tweet._json)
            break
        except Timeout:
            logging.error("Timeout error while fetching tweets. Retrying...")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Error fetching tweets: {e}")
            return
    else:
        logging.error(f"Failed to fetch tweets after {max_retries} attempts.")
        return
