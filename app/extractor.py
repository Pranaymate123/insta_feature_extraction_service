import httpx
import logging
from app.config import APIFY_API_TOKEN, APIFY_TASK_ID, SPAM_WORDS, SUSPICIOUS_WORDS
from app.utils import *

logging.basicConfig(level=logging.INFO)


async def extract_features_from_instagram(profile_url: str) -> dict:
    url = f"https://api.apify.com/v2/actor-tasks/{APIFY_TASK_ID}/run-sync-get-dataset-items?token={APIFY_API_TOKEN}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()[0]
    except Exception as e:
        logging.error(f"Error fetching from Apify for {profile_url}: {e}")
        return {"error": str(e)}

    bio = data.get("biography", "")
    followers = data.get("followersCount", 0)
    follows = data.get("followsCount", 1)
    posts = data.get("postsCount", 0)
    highlight_reels = data.get("highlightReelCount", 0)

    features = {
        "username_length": len(data.get("username", "")),
        "num_digits_in_username": count_digits(data.get("username", "")),
        "profile_has_picture": int(bool(data.get("profilePicUrlHD"))),
        "profile_has_bio": int(bool(bio.strip())),
        "bio_word_count": len(bio.split()),
        "spam_word_count": count_word_occurrences(bio, SPAM_WORDS),
        "suspicious_words_in_bio": count_word_occurrences(bio, SUSPICIOUS_WORDS),
        "bio_sentiment_score": sentiment_score(bio),
        "followers_count": followers,
        "follows_count": follows,
        "friend_follower_ratio": round(follows / (followers + 1e-5), 2),
        "posts_count": posts,
        "activity_score": round((posts + highlight_reels) / (followers + 1), 2),
        "joined_recently": int(data.get("joinedRecently", False)),
        "is_verified": int(data.get("verified", False)),
    }
    return features
