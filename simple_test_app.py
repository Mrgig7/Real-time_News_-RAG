import streamlit as st
import sys
import os

# Add path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.title("🗞️ Simple News RAG Test")

st.write("This is a simplified version to test the basic functionality.")

if st.button("Test Basic Import"):
    try:
        st.write("Testing imports...")
        
        # Test basic imports
        from app.ingest import fetch_rss_articles
        st.success("✅ Successfully imported fetch_rss_articles")
        
        # Test fetching articles
        st.write("Fetching articles...")
        articles = fetch_rss_articles()
        st.success(f"✅ Fetched {len(articles)} articles")
        
        if articles:
            st.write("**Sample Article:**")
            sample = articles[0]
            st.write(f"- Title: {sample.get('title', 'No title')}")
            st.write(f"- Source: {sample.get('source', 'Unknown')}")
            st.write(f"- Content length: {len(sample.get('text', ''))}")
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.error(f"Error type: {type(e).__name__}")
        
        import traceback
        st.code(traceback.format_exc())

if st.button("Test Simple Ingestion"):
    try:
        st.write("Testing ingestion...")
        
        from app.ingest import ingest_news
        
        with st.spinner("Ingesting 1 article..."):
            count = ingest_news(max_articles=1)
            st.success(f"✅ Ingested {count} articles")
            
    except Exception as e:
        st.error(f"❌ Ingestion Error: {e}")
        import traceback
        st.code(traceback.format_exc())

st.write("---")
st.write("**Debug Info:**")
st.write(f"- Python version: {sys.version}")
st.write(f"- Current directory: {os.getcwd()}")
st.write(f"- Python path: {sys.path[:3]}...")  # Show first 3 paths
