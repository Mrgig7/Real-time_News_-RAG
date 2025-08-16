"""
Streamlit deployment entry point for Real-time News RAG with Fact-Checking
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
try:
    # Import the main app module
    from app.main import main

    # Call the main function
    main()

except Exception as e:
    import streamlit as st
    st.error(f"Failed to load the application: {e}")
    st.error("Please check the console for detailed error information.")

    with st.expander("Debug Information"):
        st.write(f"Error type: {type(e).__name__}")
        st.write(f"Error message: {str(e)}")
        st.write(f"Python path: {sys.path}")
        st.write(f"Current directory: {os.getcwd()}")

# This file serves as the entry point for Streamlit Cloud deployment
# The actual app logic is in app/main.py
