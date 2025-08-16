from newspaper import Article
import requests
from sentence_transformers import SentenceTransformer
import chromadb
import time

NEWS_SOURCES = [
    "https://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://feeds.bbci.co.uk/news/world/rss.xml"
]


model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("news")

import feedparser

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

                # Generate embedding
                embedding = model.encode(art['text'])

                # Detect misinformation
                try:
                    misinfo_verdict, misinfo_explanation = detect_misinformation(art['text'])
                except Exception as e:
                    print(f"Misinformation detection failed for article {idx + 1}: {e}")
                    misinfo_verdict = "Unknown"
                    misinfo_explanation = "Analysis failed"

                # Add to collection
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
