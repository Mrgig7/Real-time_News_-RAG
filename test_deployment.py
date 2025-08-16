#!/usr/bin/env python3
"""
Test script to verify deployment setup
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'streamlit',
        'sentence_transformers', 
        'chromadb',
        'newspaper',
        'requests',
        'pandas',
        'sklearn',
        'bs4',
        'feedparser',
        'transformers',
        'torch',
        'openai',
        'dotenv'
    ]
    
    print("Testing module imports...")
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'newspaper':
                import newspaper
            elif module == 'bs4':
                import bs4
            elif module == 'sklearn':
                import sklearn
            else:
                __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            missing_modules.append(module)
    
    return missing_modules

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'app/main.py',
        'app/ingest.py',
        'retrieval/search.py',
        'fact_checking/check.py',
        'fact_checking/misinfo.py',
        'scoring/credibility.py'
    ]
    
    print("\nTesting file structure...")
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    return missing_files

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment...")
    
    # Check if .env.example exists
    if os.path.exists('.env.example'):
        print("✓ .env.example exists")
    else:
        print("✗ .env.example missing")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 8):
        print("✓ Python version compatible")
    else:
        print("✗ Python version too old (requires 3.8+)")

def main():
    """Run all tests"""
    print("=== Deployment Setup Test ===\n")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")
    
    # Run tests
    missing_modules = test_imports()
    missing_files = test_file_structure()
    test_environment()
    
    # Summary
    print("\n=== Summary ===")
    if missing_modules:
        print(f"Missing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
    else:
        print("✓ All required modules available")
    
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
    else:
        print("✓ All required files present")
    
    if not missing_modules and not missing_files:
        print("\n🎉 Deployment setup looks good!")
        print("You can now deploy to Streamlit Cloud or run locally with:")
        print("streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Please fix the issues above before deploying")

if __name__ == "__main__":
    main()
