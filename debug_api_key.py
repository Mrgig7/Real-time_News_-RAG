#!/usr/bin/env python3
"""
Debug script to check API key loading in different contexts
"""

import os
import sys
from dotenv import load_dotenv

def debug_api_key():
    print("=== API Key Debug Information ===")
    
    # Check current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_file = ".env"
    print(f".env file exists: {os.path.exists(env_file)}")
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
            print(f".env file content: {content}")
    
    # Load environment variables
    print("\n--- Before load_dotenv() ---")
    print(f"GEMINI_API_KEY from os.environ: {os.environ.get('GEMINI_API_KEY', 'NOT_FOUND')}")
    
    load_dotenv()
    
    print("\n--- After load_dotenv() ---")
    print(f"GEMINI_API_KEY from os.environ: {os.environ.get('GEMINI_API_KEY', 'NOT_FOUND')}")
    print(f"GEMINI_API_KEY from os.getenv(): {os.getenv('GEMINI_API_KEY', 'NOT_FOUND')}")
    
    # Check if we can import and configure Gemini
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            print(f"\n--- Testing API Key ---")
            print(f"API Key (first 10 chars): {api_key[:10]}...")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Test a simple call
            response = model.generate_content("Say 'test' in one word")
            print(f"API Test Result: SUCCESS - {response.text}")
            
        else:
            print("No API key found!")
            
    except Exception as e:
        print(f"API Test Result: FAILED - {e}")

if __name__ == "__main__":
    debug_api_key()
