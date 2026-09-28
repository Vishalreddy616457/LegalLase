# LegalEase - AI-Powered Legal Document Generator

This implementation follows the supplied LegalEase project specification.

## Architecture
- Frontend: Streamlit
- Backend: FastAPI
- AI Core: Google Gemini
- Exports: TXT, DOCX, PDF

## Setup

```bash
python -m venv .venv
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro
```

Never upload `.env` to GitHub.

Start backend:

```bash
uvicorn main:app --reload
```

Start frontend in another terminal:

```bash
streamlit run app.py
```

Enter document type, parties, terms separated by semicolons, and effective date.
Click Generate Document, edit the result, and download TXT/DOCX/PDF.
