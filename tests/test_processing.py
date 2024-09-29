import pandas as pd
from src.processing import preprocess_data

def test_preprocess_data():
    tweets = [
        {
            "created_at": "Fri May 27 20:43:37 +0000 2022",
            "entities": {"hashtags": [{"text": "FlixBus"}]},
            "retweeted_status": None,
            "user": {"id_str": "1", "followers_count": 100, "location": "NYC"},
            "text": "Test tweet"
        }
    ]
    
    df = preprocess_data(tweets)
    
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df['user_id'][0] == "1"
    assert df['followers_count'][0] == 100
    assert df['tweet_length'][0] == len("Test tweet")
