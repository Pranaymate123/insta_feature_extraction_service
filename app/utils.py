import re
from textblob import TextBlob
from app.config import SUSPICIOUS_WORDS, SPAM_WORDS

# Function to count digits in the text
def count_digits(text: str) -> int:
    return sum(char.isdigit() for char in text)

# Function to count occurrences of suspicious words in the text
def count_word_occurrences(text: str, words: list) -> int:
    return sum(word.lower() in text.lower() for word in words)

# Function to calculate the sentiment score of the text
def sentiment_score(text: str) -> float:
    return TextBlob(text).sentiment.polarity

# Function to extract hashtags from the text
def extract_hashtags(text: str) -> int:
    return len(re.findall(r"#\w+", text))

# Function to extract mentions from the text
def extract_mentions(text: str) -> int:
    return len(re.findall(r"@\w+", text))

# Function to extract URLs from the text
def extract_urls(text: str) -> int:
    return len(re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text))

# Function to check for the presence of external URLs (e.g., suspicious links in bio)
def extract_external_urls(text: str) -> int:
    return len(re.findall(r"(?i)\b(?:https?|ftp):\/\/[^\s/$.?#].[^\s]*\b", text))

