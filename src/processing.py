import logging
import pandas as pd

from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)


def validate_tweet_schema(tweet: dict) -> bool:
    required_fields = ['created_at', 'entities', 'user', 'text']
    return all(field in tweet for field in required_fields)


def preprocess_data(tweets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Process raw tweet data to extract and filter relevant information for tweets containing the '#FlixBus' hashtag.

    Args:
        tweets (List[Dict[str, Any]]): A list of dictionaries, where each dictionary
            contains raw data of a single tweet.

    Returns:
        pd.DataFrame: A DataFrame containing processed data about tweets including
            datetime of tweet, hashtags used, retweet status, user ID, follower count,
            user location, and length of the tweet text. Only includes tweets with the
            '#FlixBus' hashtag.
    """
    logging.info(f"Starting data preprocessing for {len(tweets)} tweets.")

    target_hashtag = 'flixbus'
    valid_tweets = [tweet for tweet in tweets if validate_tweet_schema(tweet)]
    
    if not valid_tweets:
        logging.error("No valid tweets found due to schema mismatch.")
        return pd.DataFrame()

    processed_tweets = [
        {
            'datetime': tweet['created_at'],
            'hashtags': [tag['text'] for tag in tweet['entities']['hashtags']],
            'is_retweet': 'retweeted_status' in tweet,
            'user_id': tweet['user']['id_str'],
            'followers_count': tweet['user']['followers_count'],
            'location': tweet['user']['location'],
            'tweet_length': len(tweet['text'])
        }
        for tweet in tweets
        if target_hashtag in [tag['text'].lower() for tag in tweet['entities']['hashtags']]
    ]
    
    logging.info(f"Preprocessing completed. {len(valid_tweets)} tweets are valid for analysis.")
    return pd.DataFrame(processed_tweets)
