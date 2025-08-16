#!/usr/bin/env python3
"""
Comprehensive API key testing to identify the exact issue
"""

import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

def test_api_key_comprehensive():
    print("=== Comprehensive API Key Testing ===")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"✓ API key loaded: {api_key[:10]}...")
    print(f"✓ API key length: {len(api_key)}")
    print(f"✓ API key format check: {'✓' if api_key.startswith('AIza') else '❌'}")
    
    # Test 1: Direct REST API call
    print("\n--- Test 1: Direct REST API Call ---")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": "Say hello"}]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✓ Direct REST API call successful")
        else:
            print(f"❌ Direct REST API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ REST API error: {e}")
    
    # Test 2: Python SDK
    print("\n--- Test 2: Python SDK ---")
    try:
        genai.configure(api_key=api_key)
        
        # List available models
        print("Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Test generation
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in one word")
        print(f"✓ SDK call successful: {response.text}")
        
    except Exception as e:
        print(f"❌ SDK error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Check specific error types
        if "API_KEY_INVALID" in str(e):
            print("🔍 This is specifically an API key validation error")
        elif "quota" in str(e).lower():
            print("🔍 This appears to be a quota/billing issue")
        elif "permission" in str(e).lower():
            print("🔍 This appears to be a permissions issue")
    
    # Test 3: Check API key restrictions
    print("\n--- Test 3: API Key Info ---")
    try:
        # Try to get API info
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✓ API key can access model list")
        elif response.status_code == 403:
            print("❌ API key has insufficient permissions (403)")
        elif response.status_code == 400:
            print("❌ API key is invalid (400)")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API info error: {e}")

if __name__ == "__main__":
    test_api_key_comprehensive()
