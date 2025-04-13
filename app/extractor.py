import httpx
from app.config import APIFY_API_TOKEN, APIFY_TASK_ID
from app.utils import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


async def extract_features_from_instagram(profile_url: str) -> dict:
    url = f"https://api.apify.com/v2/actor-tasks/{APIFY_TASK_ID}/run-sync-get-dataset-items?token={APIFY_API_TOKEN}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:  # Set timeout to 30 seconds
            response = await client.get(url)
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes

            data = response.json()[0]  # Take the first item from the dataset

    except httpx.TimeoutException:
        logging.error(f"Request to Apify API timed out. URL: {url}")
        return {"error": "Request timed out"}

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code}. URL: {url}")
        return {"error": f"HTTP error occurred: {e.response.status_code}"}

    except httpx.RequestError as e:
        logging.error(f"An error occurred while requesting {url}: {e}")
        return {"error": f"An error occurred: {e}"}

    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        return {"error": "An unexpected error occurred"}

    # Extract data from the response
    username = data.get("username", "")
    bio = data.get("biography", "")
    followers = data.get("followersCount", 0)
    follows = data.get("followsCount", 1)
    posts = data.get("postsCount", 0)
    highlight_reels = data.get("highlightReelCount", 0)

    # Calculate features
    features = {
        "username_length": len(username),
        "num_digits_in_username": count_digits(username),
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
