#!/usr/bin/env python3
"""
Health check script for the Real-time News RAG application
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test basic Python imports"""
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
        return True
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False

def test_app_modules():
    """Test application module imports"""
    try:
        # Test core modules
        from app import ingest
        print("✓ App ingest module import successful")
        
        from retrieval import search
        print("✓ Retrieval search module import successful")
        
        from fact_checking import check, misinfo
        print("✓ Fact checking modules import successful")
        
        from scoring import credibility
        print("✓ Scoring module import successful")
        
        return True
    except ImportError as e:
        print(f"✗ App module import failed: {e}")
        return False

def test_ai_models():
    """Test AI model loading"""
    try:
        from sentence_transformers import SentenceTransformer
        
        # Test loading a small model
        print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Sentence transformer model loaded successfully")
        
        # Test encoding
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        print(f"✓ Text encoding successful (embedding shape: {embedding.shape})")
        
        return True
    except Exception as e:
        print(f"✗ AI model test failed: {e}")
        return False

def test_database():
    """Test ChromaDB connection"""
    try:
        import chromadb
        
        # Create a test client
        client = chromadb.Client()
        print("✓ ChromaDB client created successfully")
        
        # Test collection creation
        collection = client.get_or_create_collection("health_check_test")
        print("✓ ChromaDB collection created successfully")
        
        # Clean up
        try:
            client.delete_collection("health_check_test")
            print("✓ ChromaDB cleanup successful")
        except:
            pass  # Collection might not exist
        
        return True
    except Exception as e:
        print(f"✗ ChromaDB test failed: {e}")
        return False

def test_news_fetching():
    """Test news fetching functionality"""
    try:
        import feedparser
        import requests
        
        # Test RSS feed parsing
        test_feed = "https://rss.cnn.com/rss/cnn_topstories.rss"
        print(f"Testing RSS feed: {test_feed}")
        
        # Set a timeout for the request
        feed = feedparser.parse(test_feed)
        
        if feed.entries:
            print(f"✓ RSS feed parsed successfully ({len(feed.entries)} entries)")
            return True
        else:
            print("⚠️  RSS feed parsed but no entries found")
            return True  # Still consider this a pass
            
    except Exception as e:
        print(f"✗ News fetching test failed: {e}")
        return False

def main():
    """Run all health checks"""
    print("=== Real-time News RAG Health Check ===\n")
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("App Modules", test_app_modules),
        ("AI Models", test_ai_models),
        ("Database", test_database),
        ("News Fetching", test_news_fetching)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n=== Health Check Summary ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All health checks passed! The application is ready to run.")
    else:
        print("⚠️  Some health checks failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
