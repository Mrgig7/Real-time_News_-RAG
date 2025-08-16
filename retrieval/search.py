import json
import os
from fact_checking.check import fact_check
from scoring.credibility import get_source_credibility

# Try to import heavy dependencies, fallback if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    model = None
    print("Warning: sentence-transformers not available, using keyword-based search")

try:
    import chromadb
    CHROMADB_AVAILABLE = True
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("news")
except ImportError:
    CHROMADB_AVAILABLE = False
    collection = None
    print("Warning: chromadb not available, using fallback storage")

FALLBACK_STORAGE_FILE = "news_articles.json"

def load_fallback_storage():
    """Load articles from fallback JSON storage"""
    if os.path.exists(FALLBACK_STORAGE_FILE):
        try:
            with open(FALLBACK_STORAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading fallback storage: {e}")
    return []

def keyword_search(query, articles, top_k=3):
    """Simple keyword-based search as fallback"""
    query_words = query.lower().split()
    scored_articles = []

    for article in articles:
        text = (article.get('title', '') + ' ' + article.get('text', '')).lower()
        score = sum(1 for word in query_words if word in text)
        if score > 0:
            scored_articles.append((score, article))

    # Sort by score and return top_k
    scored_articles.sort(key=lambda x: x[0], reverse=True)
    return [article for score, article in scored_articles[:top_k]]

def search_news(query, top_k=3):
    """Search news articles using available storage method"""
    output = []

    if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
        # Use ChromaDB with embeddings
        try:
            query_emb = model.encode(query)
            results = collection.query(query_embeddings=[query_emb.tolist()], n_results=top_k)

            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                credibility = get_source_credibility(meta['source'])
                fact, evidence = fact_check(query, doc)
                output.append({
                    'source': meta['source'],
                    'credibility': credibility,
                    'fact_check': fact,
                    'evidence': evidence,
                    'context': doc,
                    'misinfo_verdict': meta.get('misinfo_verdict', 'Unknown'),
                    'misinfo_explanation': meta.get('misinfo_explanation', '')
                })
        except Exception as e:
            print(f"ChromaDB search failed: {e}")
            # Fall back to keyword search
            return search_news_fallback(query, top_k)
    else:
        # Use fallback keyword search
        return search_news_fallback(query, top_k)

    return output

def search_news_fallback(query, top_k=3):
    """Fallback search using keyword matching"""
    articles = load_fallback_storage()

    if not articles:
        print("No articles found in fallback storage")
        return []

    # Use keyword search
    relevant_articles = keyword_search(query, articles, top_k)

    output = []
    for article in relevant_articles:
        credibility = get_source_credibility(article.get('source', 'Unknown'))
        fact, evidence = fact_check(query, article.get('text', ''))

        output.append({
            'source': article.get('source', 'Unknown'),
            'credibility': credibility,
            'fact_check': fact,
            'evidence': evidence,
            'context': article.get('text', '')[:500] + '...',  # Truncate for display
            'misinfo_verdict': article.get('misinfo_verdict', 'Unknown'),
            'misinfo_explanation': article.get('misinfo_explanation', '')
        })

    return output
