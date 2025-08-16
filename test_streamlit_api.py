#!/usr/bin/env python3
"""
Test script to replicate the exact API loading scenario in Streamlit context
"""

import sys
import os

# Add the current directory to Python path (same as streamlit_app.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_loading():
    print("=== Testing API Loading in Streamlit Context ===")
    
    # Test 1: Direct import and test
    print("\n1. Testing direct import...")
    try:
        from fact_checking.misinfo import detect_misinformation
        from fact_checking.check import fact_check
        print("✓ Modules imported successfully")
        
        # Test misinformation detection
        print("\n2. Testing misinformation detection...")
        test_article = "This is a test article about climate change and its effects on weather patterns."
        verdict, explanation = detect_misinformation(test_article)
        print(f"Verdict: {verdict}")
        print(f"Explanation: {explanation}")
        
        # Test fact checking
        print("\n3. Testing fact checking...")
        test_query = "Climate change affects weather"
        test_context = "Climate change is known to influence global weather patterns through various mechanisms."
        fact_verdict, fact_explanation = fact_check(test_query, test_context)
        print(f"Fact Check Verdict: {fact_verdict}")
        print(f"Fact Check Explanation: {fact_explanation}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_loading()
