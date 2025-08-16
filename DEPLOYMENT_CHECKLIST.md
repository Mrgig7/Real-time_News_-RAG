# Deployment Checklist

## Pre-Deployment Checklist

### ✅ Files Created/Updated
- [x] `streamlit_app.py` - Entry point for Streamlit Cloud
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `.streamlit/secrets.toml` - Template for secrets (local dev only)
- [x] `.env.example` - Environment variables template
- [x] `requirements.txt` - Updated with version pins
- [x] `DEPLOYMENT.md` - Detailed deployment guide
- [x] `packages.txt` - System dependencies
- [x] `test_deployment.py` - Deployment verification script
- [x] `health_check.py` - Application health check
- [x] Updated `README.md` with deployment instructions

### ✅ Code Changes
- [x] Fixed import paths in `app/main.py`
- [x] Added Streamlit secrets support in `fact_checking/check.py`
- [x] Added Streamlit secrets support in `fact_checking/misinfo.py`
- [x] Updated requirements with proper version constraints

## Deployment Steps

### 1. Local Testing
```bash
# Test deployment setup
python test_deployment.py

# Run health check
python health_check.py

# Test the app locally
streamlit run streamlit_app.py
```

### 2. GitHub Repository
- [ ] Push all changes to GitHub
- [ ] Ensure repository is public or accessible to Streamlit Cloud
- [ ] Verify all files are committed

### 3. Streamlit Cloud Deployment
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Click "New app"
- [ ] Connect GitHub repository
- [ ] Set main file path: `streamlit_app.py`
- [ ] Configure secrets in app settings:
  ```toml
  GEMINI_API_KEY = "your_actual_api_key_here"
  ```
- [ ] Deploy the app

### 4. Post-Deployment Verification
- [ ] App loads without errors
- [ ] News ingestion works
- [ ] Fact-checking functionality works
- [ ] Search and retrieval works
- [ ] UI displays correctly

## Required API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to Streamlit secrets as `GEMINI_API_KEY`

## Troubleshooting

### Common Issues
1. **Import Errors**: Check that all modules are in `requirements.txt`
2. **API Key Issues**: Verify secrets are properly configured
3. **Memory Issues**: Some models require significant memory
4. **Network Issues**: RSS feeds might be temporarily unavailable

### Fallback Behavior
- App works without API keys (limited functionality)
- Keyword-based analysis when AI fails
- Graceful error handling throughout

## Performance Considerations
- First load may be slow (model downloads)
- ChromaDB creates local storage
- RSS feeds fetched in real-time
- Caching reduces API calls

## Security Notes
- Never commit API keys to repository
- Use Streamlit secrets for sensitive data
- Environment variables as fallback
- API keys should have appropriate restrictions

## Monitoring
- Check Streamlit Cloud logs for errors
- Monitor API usage quotas
- Watch for RSS feed failures
- Track user engagement metrics
