from pymongo import MongoClient
from datetime import datetime
from scholarly import scholarly

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["the-scientefic-collector"]
papers_collection = db["scientefic-papers"]
temp_papers_collection = db["temp-papers"]

def fetch_papers(query="scientific papers"):
    """
    Fetches scientific papers using the scholarly library.
    """
    search_query = scholarly.search_pubs(query)
    papers = []
    for paper in search_query:
        paper_data = scholarly.fill(paper)
        papers.append({
            "title": paper_data["bib"]["title"],
            "author": paper_data["bib"].get("author", "N/A"),
            "publishedAt": paper_data["bib"].get("pub_year", datetime.utcnow().year),
            "url": paper_data.get("eprint_url", ""),
            "abstract": paper_data["bib"].get("abstract", ""),
            "journal": paper_data["bib"].get("journal", "N/A")
        })
    return papers

def store_papers(papers):
    """
    Stores scraped scientific papers in MongoDB with the new data structure.
    """
    formatted_papers = []

    for paper in papers:
        if not papers_collection.find_one({"title": paper["title"]}):
            formatted_papers.append(paper)

    if formatted_papers:
        papers_collection.insert_many(formatted_papers)
        print(f"✅ Successfully inserted {len(formatted_papers)} papers into MongoDB.")
    else:
        print(f"⚠ No valid papers to insert.")

def fetch_and_store_temp_papers():
    """
    Fetches papers and stores them in a temporary collection.
    """
    papers = fetch_papers()
    temp_papers_collection.insert_many(papers)
    print(f"✅ Successfully fetched and stored {len(papers)} papers in the temporary collection.")

def store_temp_papers():
    """
    Stores papers from the temporary collection into the main collection.
    """
    temp_papers = list(temp_papers_collection.find())
    store_papers(temp_papers)
    temp_papers_collection.delete_many({})
    print(f"✅ Successfully moved {len(temp_papers)} papers from the temporary collection to the main collection.")
