import pandas as pd

from typing import List, Dict, Any


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
    target_hashtag = 'flixbus'

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

    return pd.DataFrame(processed_tweets)
