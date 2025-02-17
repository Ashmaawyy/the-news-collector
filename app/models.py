from config import COLLECTION_NAME
from app import db
from datetime import datetime

news_collection = db[COLLECTION_NAME]

def store_headlines(source, articles):
    """
    Stores scraped news articles in MongoDB with the new data structure.
    """
    formatted_articles = []

    for article in articles:
        data = {
            "name": source,  # News source name (e.g., BBC, CNN)
            "headline": article.get("headline", "N/A"),
            "article_url": article.get("article_url", "N/A"),
            "publication_date": article.get("publication_date", datetime.utcnow()),  # Default to now if missing
            "author": article.get("author", "N/A"),
            "summary": article.get("summary", "N/A"),
            "category": article.get("category", "N/A"),
            "image_url": article.get("image_url", "N/A"),
            "keywords": article.get("keywords", "").split(", ") if "keywords" in article else []
        }
        formatted_articles.append(data)

    if formatted_articles:
        news_collection.insert_many(formatted_articles)
        print(f"✅ Successfully inserted {len(formatted_articles)} articles from {source} into MongoDB.")
    else:
        print(f"⚠ No valid articles to insert for {source}.")


def get_latest_headlines(limit=5):
    """
    Fetches the latest news articles from MongoDB.
    Returns a list of structured articles sorted by publication date.
    """
    latest_news = list(
        news_collection.find({}, {"_id": 0})  # Exclude MongoDB _id field
        .sort("publication_date", -1)  # Sort by latest publication date
        .limit(limit)  # Limit results
    )

    return latest_news
