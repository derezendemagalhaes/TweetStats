import pandas as pd
from src.analysis import analyze_data

def test_analyze_data():
    data = {
        "datetime": ["Wed Sep 29 20:35:16 +0000 2021"],
        "hashtags": [["FlixBus"]],
        "is_retweet": [False],
        "user_id": ["123"],
        "followers_count": [100],
        "location": ["Germany"],
        "tweet_length": [15]
    }
    processed_tweets = pd.DataFrame(data)
    
    general_results, user_results = analyze_data(processed_tweets)
    
    assert isinstance(general_results, pd.DataFrame), "General results should be a DataFrame."
    assert general_results["most_active_day"].iloc[0] == pd.to_datetime("2021-09-29").date(), "Most active day calculation failed."
    
    assert isinstance(user_results, pd.DataFrame), "User results should be a DataFrame."
    assert user_results["average_tweet_length"].iloc[0] == 15, "Average tweet length calculation failed."
