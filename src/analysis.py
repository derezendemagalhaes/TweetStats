import pandas as pd
from collections import Counter
from typing import Tuple


def find_most_active_day(tweets: pd.DataFrame) -> pd.Timestamp:
    """
    Determine the day with the highest number of tweets.

    Args:
        tweets (pd.DataFrame): A DataFrame containing tweets with a 'date' column.

    Returns:
        pd.Timestamp: The day with the highest number of tweets.
    """
    return tweets['date'].value_counts().idxmax()


def count_tweets_with_minimum_hashtags(tweets: pd.DataFrame, min_hashtags: int) -> int:
    """
    Count tweets that contain at least a specified number of hashtags.

    Args:
        tweets (pd.DataFrame): DataFrame containing tweet data with a 'hashtags' column.
        min_hashtags (int): Minimum number of hashtags required to be counted.

    Returns:
        int: Number of tweets meeting the hashtag criteria.
    """
    return tweets[tweets['hashtags'].apply(len) >= min_hashtags].shape[0]


def find_max_tweets_per_user(tweets: pd.DataFrame) -> int:
    """
    Identify the maximum number of tweets posted by a single user.

    Args:
        tweets (pd.DataFrame): DataFrame containing tweet data with a 'user_id' column.

    Returns:
        int: Maximum number of tweets by a single user.
    """
    return tweets['user_id'].value_counts().max()


def prepare_user_details(tweets: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare detailed user data including their most recent activity and top hashtags used.

    Args:
        tweets (pd.DataFrame): DataFrame containing tweets sorted by datetime.

    Returns:
        pd.DataFrame: DataFrame indexed by 'user_id' with columns for recent activity and top hashtags.
    """
    latest_tweets = tweets.sort_values(by='datetime', ascending=False).drop_duplicates('user_id')
    latest_tweets.set_index('user_id', inplace=True)
    latest_tweets['average_tweet_length'] = tweets.groupby('user_id')['tweet_length'].mean()
    latest_tweets['top_five_hashtags'] = extract_top_hashtags(tweets)

    if 'tweet_length' in latest_tweets.columns:
        latest_tweets = latest_tweets.drop(columns=['tweet_length'])

    return latest_tweets


def extract_top_hashtags(tweets: pd.DataFrame) -> pd.Series:
    """
    Extract and count the top five hashtags used by each user.

    Args:
        tweets (pd.DataFrame): DataFrame of tweets with a 'hashtags' column.

    Returns:
        pd.Series: Series indexed by 'user_id' with each entry containing a list of top five hashtags.
    """
    exploded_hashtags = tweets.explode('hashtags')
    return exploded_hashtags.groupby('user_id')['hashtags'].apply(
        lambda x: [hashtag for hashtag, _ in Counter(x).most_common(5)])


def analyze_data(processed_tweets: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyze the processed tweet data to generate insights and statistics.

    Args:
        processed_tweets (pd.DataFrame): DataFrame containing processed tweet data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
        - The first DataFrame includes general statistics such as the most active day,
          the total number of tweets with at least three hashtags, and the maximum number of tweets by a single user.
        - The second DataFrame provides detailed information per user, including the most recent
          number of followers, most recent location, average tweet length, and top five hashtags used.
    """
    processed_tweets['date'] = pd.to_datetime(processed_tweets['datetime'], format='%a %b %d %H:%M:%S %z %Y').dt.date
    most_active_day = find_most_active_day(processed_tweets)
    tweets_with_three_hashtags = count_tweets_with_minimum_hashtags(processed_tweets, min_hashtags=3)
    max_tweets_per_user = find_max_tweets_per_user(processed_tweets)
    user_details = prepare_user_details(processed_tweets)
    general_statistics = pd.DataFrame({
        "Most Active Day": [most_active_day],
        "Total Tweets with >=3 Hashtags": [tweets_with_three_hashtags],
        "Max Tweets by Single User": [max_tweets_per_user]
    })

    return general_statistics, user_details
