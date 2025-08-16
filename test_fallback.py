#!/usr/bin/env python3
"""
Test script to verify fallback functionality works without heavy dependencies
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test basic imports that should work"""
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
        
        import requests
        print("✓ Requests import successful")
        
        import pandas as pd
        print("✓ Pandas import successful")
        
        import feedparser
        print("✓ Feedparser import successful")
        
        import google.generativeai as genai
        print("✓ Google Generative AI import successful")
        
        return True
    except ImportError as e:
        print(f"✗ Basic import failed: {e}")
        return False

def test_app_modules():
    """Test app modules with fallback handling"""
    try:
        # Test ingestion module
        from app.ingest import fetch_rss_articles, ingest_news
        print("✓ Ingest module import successful")
        
        # Test search module
        from retrieval.search import search_news, search_news_fallback
        print("✓ Search module import successful")
        
        # Test fact checking modules
        from fact_checking.check import fact_check
        from fact_checking.misinfo import detect_misinformation
        print("✓ Fact checking modules import successful")
        
        return True
    except ImportError as e:
        print(f"✗ App module import failed: {e}")
        return False

def test_fallback_functionality():
    """Test that fallback functions work"""
    try:
        # Test RSS fetching (should work without heavy dependencies)
        from app.ingest import fetch_rss_articles
        print("Testing RSS fetch...")
        articles = fetch_rss_articles()
        print(f"✓ Fetched {len(articles)} articles from RSS")
        
        # Test fallback search
        from retrieval.search import search_news_fallback, load_fallback_storage
        print("✓ Fallback search functions available")
        
        return True
    except Exception as e:
        print(f"✗ Fallback functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Streamlit Cloud deployment readiness...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing basic imports...")
    success &= test_basic_imports()
    
    print("\n2. Testing app modules...")
    success &= test_app_modules()
    
    print("\n3. Testing fallback functionality...")
    success &= test_fallback_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! App should deploy successfully to Streamlit Cloud.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
