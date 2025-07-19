# AI Chatbot (Anthropic Haiku)

A full-stack AI chatbot using FastAPI (backend), Streamlit (frontend), and Anthropic Haiku LLM.

## Features
- Real-time chat interface (Streamlit)
- FastAPI backend with async endpoints
- Anthropic Haiku LLM integration
- Loading indicators, chat history, and error handling
- Environment config for API keys

## Setup
1. **Clone the repo and navigate to the project directory.**
2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Create a `.env` file in the project root:**
   ```
   ANTHROPIC_API_KEY=your-anthropic-key-here
   ANTHROPIC_MODEL=haiku
   ```

## Running the App

### 1. Start the FastAPI backend:
```
uvicorn main:app --reload
```

### 2. In a new terminal, start the Streamlit frontend:
```
streamlit run app.py
```

- The Streamlit app will open in your browser (default: http://localhost:8501)
- The backend runs at http://localhost:8000

## Notes
- Make sure your Anthropic API key is valid and has access to the Haiku model.
- For production, set proper CORS origins and secure your API keys. 