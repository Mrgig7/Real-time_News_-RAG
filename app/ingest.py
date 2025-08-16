from newspaper import Article
import requests
import time
import json
import os

# Try to import heavy dependencies, fallback if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available, using fallback storage")

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: chromadb not available, using fallback storage")

NEWS_SOURCES = [
    "https://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://feeds.bbci.co.uk/news/world/rss.xml"
]

# Initialize components based on availability
if SENTENCE_TRANSFORMERS_AVAILABLE:
    model = SentenceTransformer('all-MiniLM-L6-v2')
else:
    model = None

if CHROMADB_AVAILABLE:
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("news")
else:
    # Fallback: use simple file-based storage
    collection = None
    FALLBACK_STORAGE_FILE = "news_articles.json"

import feedparser

def load_fallback_storage():
    """Load articles from fallback JSON storage"""
    if os.path.exists(FALLBACK_STORAGE_FILE):
        try:
            with open(FALLBACK_STORAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading fallback storage: {e}")
    return []

def save_to_fallback_storage(articles):
    """Save articles to fallback JSON storage"""
    try:
        with open(FALLBACK_STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to fallback storage: {e}")
        return False

def fetch_rss_articles():
    articles = []
    print("Fetching articles from RSS feeds...")

    for feed_url in NEWS_SOURCES:
        try:
            print(f"Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)

            if not feed.entries:
                print(f"No entries found in feed: {feed_url}")
                continue

            print(f"Found {len(feed.entries)} entries in feed")

            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                url = entry.link
                try:
                    article = Article(url)
                    article.download()
                    article.parse()

                    if article.text and len(article.text.strip()) > 100:  # Ensure we have substantial content
                        articles.append({
                            "title": article.title or "No title",
                            "text": article.text,
                            "url": url,
                            "source": feed.feed.title if hasattr(feed.feed, 'title') else "Unknown"
                        })
                        print(f"Successfully parsed: {article.title[:50]}...")
                    else:
                        print(f"Skipped article with insufficient content: {url}")

                except Exception as e:
                    print(f"Failed to parse article {url}: {e}")
                    continue  # Skip articles that fail to download/parse

        except Exception as e:
            print(f"Failed to fetch feed {feed_url}: {e}")
            continue

    print(f"Total articles fetched: {len(articles)}")
    return articles

from fact_checking.misinfo import detect_misinformation

def ingest_news(max_articles=5, progress_callback=None):
    try:
        print(f"Starting news ingestion for {max_articles} articles...")
        articles = fetch_rss_articles()
        print(f"Fetched {len(articles)} articles from RSS feeds")

        if not articles:
            print("No articles found from RSS feeds")
            return 0

        count = 0
        errors = 0

        for idx, art in enumerate(articles[:max_articles]):
            try:
                if progress_callback:
                    progress_callback(idx + 1, min(max_articles, len(articles)))

                print(f"Processing article {idx + 1}: {art.get('title', 'No title')[:50]}...")

                # Detect misinformation
                try:
                    misinfo_verdict, misinfo_explanation = detect_misinformation(art['text'])
                except Exception as e:
                    print(f"Misinformation detection failed for article {idx + 1}: {e}")
                    misinfo_verdict = "Unknown"
                    misinfo_explanation = "Analysis failed"

                # Store article based on available storage
                if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
                    # Use ChromaDB with embeddings
                    embedding = model.encode(art['text'])
                    collection.add(
                        ids=[art['url']],
                        documents=[art['text']],
                        embeddings=[embedding.tolist()],
                        metadatas=[{
                            "title": art['title'],
                            "url": art['url'],
                            "source": art['source'],
                            "misinfo_verdict": misinfo_verdict,
                            "misinfo_explanation": misinfo_explanation
                        }]
                    )
                else:
                    # Use fallback storage
                    existing_articles = load_fallback_storage()

                    # Check if article already exists
                    if not any(existing['url'] == art['url'] for existing in existing_articles):
                        article_data = {
                            "title": art['title'],
                            "text": art['text'],
                            "url": art['url'],
                            "source": art['source'],
                            "misinfo_verdict": misinfo_verdict,
                            "misinfo_explanation": misinfo_explanation,
                            "timestamp": time.time()
                        }
                        existing_articles.append(article_data)
                        save_to_fallback_storage(existing_articles)

                count += 1
                print(f"Successfully processed article {idx + 1}")

            except Exception as e:
                errors += 1
                print(f"Error processing article {idx + 1}: {e}")
                continue

        print(f"Ingestion completed: {count} successful, {errors} errors")
        return count

    except Exception as e:
        print(f"Critical error in ingest_news: {e}")
        raise e

if __name__ == "__main__":
    articles = fetch_rss_articles()
    print(f"Fetched {len(articles)} articles.")
    for a in articles[:2]:
        print(a['title'], a['url'])
