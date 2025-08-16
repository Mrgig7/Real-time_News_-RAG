#!/usr/bin/env python3
"""
Simple test script to verify news ingestion works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ingestion():
    print("=== Testing News Ingestion ===")
    
    try:
        from app.ingest import fetch_rss_articles, ingest_news
        
        print("1. Testing RSS article fetching...")
        articles = fetch_rss_articles()
        print(f"   ✓ Fetched {len(articles)} articles")
        
        if articles:
            print("   Sample article:")
            sample = articles[0]
            print(f"   - Title: {sample.get('title', 'No title')[:100]}...")
            print(f"   - Source: {sample.get('source', 'Unknown')}")
            print(f"   - URL: {sample.get('url', 'No URL')}")
            print(f"   - Content length: {len(sample.get('text', ''))}")
        
        print("\n2. Testing news ingestion (1 article)...")
        
        def progress_callback(current, total):
            print(f"   Progress: {current}/{total}")
        
        count = ingest_news(max_articles=1, progress_callback=progress_callback)
        print(f"   ✓ Successfully ingested {count} articles")
        
        print("\n🎉 All tests passed! The ingestion system is working.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ingestion()
    sys.exit(0 if success else 1)
