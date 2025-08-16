#!/usr/bin/env python3
"""
Test script to verify Gemini API key is working
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_api():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"✓ API key loaded: {api_key[:10]}...")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("✓ Model created successfully")
        
        # Test a simple generation
        print("Testing API call...")
        response = model.generate_content("Say hello in one word")
        
        print(f"✓ API call successful!")
        print(f"Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        if "API_KEY_INVALID" in str(e):
            print("🔧 The API key appears to be invalid")
        elif "quota" in str(e).lower():
            print("🔧 API quota exceeded")
        elif "permission" in str(e).lower():
            print("🔧 Permission denied - check API key permissions")
        
        return False

if __name__ == "__main__":
    print("=== Testing Gemini API Key ===")
    success = test_gemini_api()
    
    if success:
        print("\n🎉 API key is working correctly!")
    else:
        print("\n⚠️ API key test failed. Please check your key and try again.")
