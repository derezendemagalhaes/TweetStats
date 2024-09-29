import os
import tweepy
import datetime
import json
import logging

from typing import Any, Dict, List
from dotenv import load_dotenv

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


def get_tweets(days=7):
    """
    Retrieve tweets from the last `days` days containing the hashtag #FlixBus.

    Args:
        days (int): The number of days from which to fetch tweets.

    Returns:
        None: Tweets are saved to a file and errors are logged.
    """
    load_dotenv()

    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    since_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    until_date = datetime.datetime.now().strftime("%Y-%m-%d")

    hashtag = "#flixbus"
    tweets_data = []
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=hashtag, since=since_date, until=until_date, lang='en').items()
        for tweet in tweets:
            tweets_data.append(tweet._json)
    except Exception as e:
        logging.error(f"Error fetching tweets: {e}")
        return

    file_name = 'tweets_api.json'
    try:
        with open(file_name, 'w') as json_file:
            json.dump(tweets_data, json_file, indent=4)
        logging.info(f"Data successfully retrieved and saved to {file_name}")
    except IOError as e:
        logging.error(f"Error saving tweets to {file_name}: {e}")
