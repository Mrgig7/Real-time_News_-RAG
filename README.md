# Real-time News RAG with Fact-Checking

## Overview
A Retrieval-Augmented Generation (RAG) system for real-time news ingestion, misinformation detection, fact-checking, and source credibility scoring. Built with Streamlit, HuggingFace Sentence Transformers, and ChromaDB.

## Features
- Real-time news ingestion
- Misinformation detection
- Source credibility scoring
- Fact-checking with evidence retrieval
- User-friendly web interface

##ScreenShot of Working Demo 
<img width="1366" height="683" alt="Screenshot (892)" src="https://github.com/user-attachments/assets/0e224ffd-5fbd-46d2-a2d5-5209168f0463" />
<img width="1366" height="666" alt="Screenshot (894)" src="https://github.com/user-attachments/assets/9d5d8254-8ddd-4f22-b652-69feeeb560ab" />
<img width="1366" height="602" alt="image" src="https://github.com/user-attachments/assets/4a18baae-7f9b-4084-a4ad-0c0726b820af" />
<img width="1366" height="673" alt="Screenshot (897)" src="https://github.com/user-attachments/assets/39f9eb4e-3b9d-4109-a1c7-95d67b0dabc4" />





## Setup

### Local Development
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy environment file: `cp .env.example .env`
4. Add your API keys to `.env` file
5. Run the app: `streamlit run streamlit_app.py`

### API Keys Required
- **Google Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Add to `.env` file or Streamlit secrets

## Project Structure
- `app/` – Streamlit UI
- `retrieval/` – Vector DB and retrieval logic
- `fact_checking/` – Fact-checking modules
- `scoring/` – Source credibility scoring
- `utils/` – Shared utilities
- `streamlit_app.py` – Deployment entry point
- `.streamlit/` – Streamlit configuration

## Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `streamlit_app.py`
5. Add API keys in app secrets
6. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Other Platforms
- **Heroku**: Use `streamlit_app.py` as entry point
- **Railway**: Compatible with current setup
- **Render**: Works with Streamlit configuration
