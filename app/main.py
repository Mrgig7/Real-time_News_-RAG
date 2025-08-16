
import streamlit as st
import time
import logging
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingest import ingest_news
from retrieval.search import search_news

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main Streamlit application function"""

    # Check for heavy dependencies and show deployment mode
    try:
        import sentence_transformers
        import chromadb
        FULL_MODE = True
        deployment_mode = "Full Mode (with AI embeddings)"
    except ImportError:
        FULL_MODE = False
        deployment_mode = "Lightweight Mode (keyword search)"
        st.info(f"🚀 Running in {deployment_mode} - optimized for cloud deployment")

    # Import cache utilities from our improved modules
    try:
        from fact_checking.check import get_cache_stats as get_fact_check_cache_stats, clear_expired_cache as clear_fact_check_cache
        from fact_checking.misinfo import get_cache_stats as get_misinfo_cache_stats, clear_expired_cache as clear_misinfo_cache
        CACHE_MODULES_AVAILABLE = True
    except ImportError:
        CACHE_MODULES_AVAILABLE = False

    # Page configuration
    st.set_page_config(
        page_title="Real-time News RAG with Fact-Checking",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1f77b4;
            padding: 1rem 0;
        }
        .status-box {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .success-box {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        .warning-box {
            background-color: #fff3cd;
            border-color: #ffeaa7;
            color: #856404;
        }
        .error-box {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main title
    st.markdown('<h1 class="main-header">🔍Real-time News RAG with Fact-Checking</h1>', unsafe_allow_html=True)

    # Sidebar for system controls and monitoring
    with st.sidebar:
        st.header("🛠️ System Controls")

        # System status
        st.subheader("📊 System Status")

        # Cache statistics (if available)
        if CACHE_MODULES_AVAILABLE:
            try:
                fact_check_stats = get_fact_check_cache_stats()
                misinfo_stats = get_misinfo_cache_stats()

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Fact-Check Cache", fact_check_stats['valid_cached'])
                with col2:
                    st.metric("Misinfo Cache", misinfo_stats['valid_cached'])

                # Cache management
                st.subheader("🧹 Cache Management")
                if st.button("Clear Expired Caches"):
                    cleared_fact = clear_fact_check_cache()
                    cleared_misinfo = clear_misinfo_cache()
                    st.success(f"Cleared {cleared_fact + cleared_misinfo} expired entries")
            except Exception as e:
                st.error(f"Cache monitoring error: {e}")

        # Settings
        st.subheader("⚙️ Settings")
        max_articles = st.slider("Max Articles to Ingest", 10, 100, 30)
        show_debug_info = st.checkbox("Show Debug Information", value=False)
        auto_refresh = st.checkbox("Auto-refresh Results", value=False)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📰 News Ingestion")

        # Ingestion section with better error handling
        ingest_col1, ingest_col2 = st.columns([3, 1])

        with ingest_col1:
            ingest_button = st.button("🔄 Ingest Latest News", type="primary")

        with ingest_col2:
            if st.button("ℹ️ Help"):
                with st.expander("How to use this system", expanded=True):
                    st.markdown("""
                    **Steps to use:**
                    1. Click 'Ingest Latest News' to fetch recent articles
                    2. Enter a query or claim in the search box
                    3. Review the fact-checking results

                    **Features:**
                    - Real-time news ingestion from multiple sources
                    - AI-powered misinformation detection
                    - Automated fact-checking with evidence
                    - Fallback systems when AI services are unavailable
                    """)

    if ingest_button:
        try:
            progress_bar = st.progress(0, text="Preparing to ingest news articles...")
            status_placeholder = st.empty()
            
            def progress_callback(current, total):
                progress = current / total if total > 0 else 0
                progress_bar.progress(progress, text=f"Ingesting article {current} of {total}")
                
                # Update status
                if current % 5 == 0:  # Update every 5 articles
                    status_placeholder.info(f"Processed {current}/{total} articles...")
            
            start_time = time.time()
            count = ingest_news(max_articles=max_articles, progress_callback=progress_callback)
            end_time = time.time()
            
            progress_bar.empty()
            status_placeholder.empty()
            
            # Success message with stats
            st.markdown(f"""
            <div class="status-box success-box">
                ✅ Successfully ingested <strong>{count}</strong> new articles in <strong>{end_time - start_time:.1f}s</strong>
            </div>
            """, unsafe_allow_html=True)
            
            logger.info(f"Ingested {count} articles in {end_time - start_time:.1f} seconds")
            
        except Exception as e:
            st.markdown(f"""
            <div class="status-box error-box">
                ❌ Error during ingestion: {str(e)}
            </div>
            """, unsafe_allow_html=True)
            logger.error(f"Ingestion failed: {e}", exc_info=True)

            # Show detailed error information
            with st.expander("🔧 Error Details & Troubleshooting"):
                st.error(f"**Error Type:** {type(e).__name__}")
                st.error(f"**Error Message:** {str(e)}")

                st.markdown("""
                **Troubleshooting Steps:**
                - Check your internet connection
                - Verify API keys are properly configured in .env file
                - Try reducing the number of articles to ingest
                - Check if all dependencies are installed correctly
                - Restart the application if needed

                **Common Issues:**
                - Network timeout: Try again in a few moments
                - API rate limits: Wait a few minutes before retrying
                - Missing dependencies: Run `pip install -r requirements.txt`
                """)

                # Show system info for debugging
                st.write("**Debug Information:**")
                st.write(f"- Python version: {sys.version}")
                st.write(f"- Working directory: {os.getcwd()}")
                st.write(f"- Environment variables: GEMINI_API_KEY {'✓' if os.getenv('GEMINI_API_KEY') else '✗'}")

            # Try to provide a simple fallback
            st.info("💡 **Quick Test:** Try clicking the button again, or restart the application.")

    with col2:
        st.header("Quick Stats")

        # Display current time
        st.metric("Current Time", datetime.now().strftime("%H:%M:%S"))

        # Placeholder for additional metrics
        if 'last_ingestion_count' not in st.session_state:
            st.session_state.last_ingestion_count = 0

        st.metric("Last Ingestion", f"{st.session_state.last_ingestion_count} articles")

    # Search and Fact-Checking Section
    st.header("🔍 Query & Fact-Check")

    # Search input with better UX
    query = st.text_input(
        "Enter your news query or claim:",
        placeholder="e.g., 'Climate change causes extreme weather' or 'Latest election results'",
        help="Enter any claim or question you'd like to fact-check against recent news"
    )

    # Search button and auto-refresh logic
    search_col1, search_col2 = st.columns([4, 1])

    with search_col1:
        search_button = st.button("🔍 Search & Fact-Check", disabled=not query)

    with search_col2:
        if auto_refresh and query:
            st.write("Auto-refreshing...")
            search_button = True

    if query and search_button:
        with st.spinner("Retrieving and fact-checking..."):
            try:
                start_time = time.time()
                results = search_news(query)
                end_time = time.time()

                if not results:
                    st.warning("No results found. Try a different query or ingest more recent news.")
                else:
                    st.success(f"Found {len(results)} relevant articles in {end_time - start_time:.1f}s")

                    # Display results
                    for i, res in enumerate(results):
                        with st.container():
                            # Header with source and credibility
                            col_source, col_cred = st.columns([3, 1])
                            with col_source:
                                st.markdown(f"### 📰 **Source:** {res.get('source', 'Unknown')}")
                            with col_cred:
                                credibility = res.get('credibility', 'N/A')
                                if isinstance(credibility, (int, float)) and credibility >= 0.8:
                                    st.success(f"Credibility: {credibility}")
                                elif isinstance(credibility, (int, float)) and credibility >= 0.5:
                                    st.warning(f"Credibility: {credibility}")
                                else:
                                    st.error(f"Credibility: {credibility}")

                            # Misinformation detection
                            misinfo_verdict = res.get('misinfo_verdict', 'Unknown')
                            misinfo_explanation = res.get('misinfo_explanation', '')

                            if misinfo_verdict == "Likely Safe":
                                st.success(f"🛡️ **Misinformation Detection:** {misinfo_verdict}")
                            elif misinfo_verdict == "Potentially Misleading":
                                st.warning(f"⚠️ **Misinformation Detection:** {misinfo_verdict}")
                            else:
                                st.error(f"🚨 **Misinformation Detection:** {misinfo_verdict}")

                            if misinfo_explanation:
                                st.markdown(f"*{misinfo_explanation}*")

                            # Fact-checking results
                            fact_check = res.get('fact_check', 'Unverified')
                            evidence = res.get('evidence', 'No evidence provided')

                            if fact_check == "Likely True":
                                st.success(f"✅ **Fact-Check:** {fact_check}")
                            elif fact_check == "Likely False":
                                st.error(f"❌ **Fact-Check:** {fact_check}")
                            else:
                                st.info(f"❓ **Fact-Check:** {fact_check}")

                            st.markdown(f"**Evidence:** {evidence}")

                            # Debug information
                            if show_debug_info or 'context' in res:
                                with st.expander("🔧 Debug Information"):
                                    if 'context' in res:
                                        st.subheader("Retrieved News Context")
                                        st.text_area("Context", res['context'], height=100, disabled=True)

                                    if show_debug_info:
                                        st.subheader("Raw Result Data")
                                        st.json(res)

                            st.markdown("---")

            except Exception as e:
                st.markdown(f"""
                <div class="status-box error-box">
                    ❌ Error during search and fact-checking: {str(e)}
                </div>
                """, unsafe_allow_html=True)
                logger.error(f"Search failed: {e}")

                # Show fallback options
                with st.expander("What you can do:"):
                    st.markdown("""
                    - Try a simpler query
                    - Check if news ingestion completed successfully
                    - Verify your API configurations
                    - The system may be using fallback methods - results might be limited but still useful
                    """)

    # Footer with system information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <small>
        🤖Powered by AI fact-checking with intelligent fallbacks |
        ⚡Real-time news ingestion |
        🛡️ Built-in misinformation detection
        </small>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh logic
    if auto_refresh and query:
        time.sleep(30)  # Refresh every 30 seconds
        st.experimental_rerun()

# Call main function when script is run
if __name__ == "__main__":
    main()
