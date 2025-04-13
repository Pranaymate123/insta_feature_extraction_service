from pydantic import BaseModel
from typing import List

class ProfileListRequest(BaseModel):
    profile_urls: List[str]

class FeatureResponse(BaseModel):
    username_length: int
    num_digits_in_username: int
    profile_has_picture: int  # changed from bool to int
    profile_has_bio: int      # changed from bool to int
    bio_word_count: int
    spam_word_count: int
    suspicious_words_in_bio: int
    bio_sentiment_score: float
    followers_count: int
    follows_count: int
    friend_follower_ratio: float
    posts_count: int
    activity_score: float
    joined_recently: int      # changed from bool to int
    is_verified: int
