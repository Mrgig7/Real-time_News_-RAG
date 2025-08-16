# Deployment Guide for Real-time News RAG

This guide covers deploying the Real-time News RAG application on Streamlit Cloud.

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Keys**: Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has these files:
- `streamlit_app.py` (entry point for Streamlit Cloud)
- `requirements.txt` (dependencies)
- `.streamlit/config.toml` (Streamlit configuration)
- `.streamlit/secrets.toml` (for local development only)

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set the main file path to `streamlit_app.py`
5. Click "Deploy"

### 3. Configure Secrets

In your Streamlit Cloud app settings:

1. Go to your app dashboard
2. Click on "Settings" → "Secrets"
3. Add your secrets in TOML format:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

### 4. Environment Variables

The app will automatically use:
- Streamlit secrets (in cloud deployment)
- `.env` file (for local development)
- Environment variables (fallback)

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Real-time_News_-RAG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the app:
```bash
streamlit run streamlit_app.py
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Key Issues**: Verify your Gemini API key is correctly set in secrets
3. **Memory Issues**: The app uses AI models that require sufficient memory

### Fallback Behavior

The app is designed with fallbacks:
- If Gemini API fails, it uses keyword-based analysis
- If models fail to load, basic functionality still works
- Graceful error handling throughout

## Features

- **Real-time News Ingestion**: Fetches from RSS feeds
- **AI-Powered Fact Checking**: Uses Google Gemini API
- **Misinformation Detection**: Automated content analysis
- **Source Credibility Scoring**: Evaluates news source reliability
- **Caching**: Improves performance and reduces API calls

## Support

For issues:
1. Check the app logs in Streamlit Cloud
2. Verify all secrets are properly configured
3. Ensure your API keys have sufficient quota
4. Check the GitHub repository for updates
