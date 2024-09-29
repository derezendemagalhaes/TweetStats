import os
import json
from src.data import load_data

def test_load_data():
    sample_data = [
        {"created_at": "Wed Sep 29 20:35:16 +0000 2021", "text": "This is a tweet", "entities": {"hashtags": [{"text": "FlixBus"}]}, "user": {"id_str": "123", "followers_count": 100, "location": "Germany"}}
    ]
    file_path = "tests/sample_tweets.json"
    with open(file_path, "w") as f:
        json.dump(sample_data, f)
    
    data = load_data(file_path)
    assert isinstance(data, list), "Data should be loaded as a list."
    assert len(data) == 1, "Data should contain one tweet."
    assert data[0]["text"] == "This is a tweet", "Tweet text does not match."
    
    os.remove(file_path)
