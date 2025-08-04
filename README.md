# AI Business Assistant

Your all-in-one AI assistant for managing multiple businesses.

## Features
- Toggle GPT-3.5 & Gemini AI
- Upload files (TXT, PDF, CSV)
- Per-business memory
- Voice output (text-to-speech)

## How to Use
### Local:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Render (Cloud):
1. Push this code to GitHub
2. Go to [https://render.com/deploy](https://render.com/deploy)
3. Connect your repo
4. Add Environment Variables:
   - `OPENAI_API_KEY`
   - `GOOGLE_API_KEY`
