# KnowledgeNest AI

KnowledgeNest AI is a simple academic companion for organizing study material, finding resources faster, and getting help with topics from your syllabus.

## What it does

- Organizes content by semester, subject, unit, and topic
- Lets you search for study resources
- Suggests related topics using machine learning
- Includes an AI chat assistant for study help
- Supports faculty uploads for sharing resources

## Stack

- Frontend: React, TypeScript, Tailwind CSS
- Backend: FastAPI, Python, SQLAlchemy
- Database: SQLite for local development
- ML: TF-IDF, K-Means, NLTK
- AI: Ollama

## Local setup

### Prerequisites

```bash
✓ Python 3.11
✓ Node.js 18+
✓ Ollama (optional, but recommended)
✓ A functioning keyboard
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed.seed_c_python
python -m app.seed.seed_python_unit1
python -m app.seed.seed_python_unit2
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment

Create `backend/.env`:

```env
DATABASE_URL=sqlite:///./academic_platform.db

# AI defaults used by normal users
AI_PROVIDER=local
AI_BASE_URL=
AI_API_KEY=
AI_MODEL=

# Ollama fallback for the local provider
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b

# Optional: unlock temporary Developer Options in Settings
# Set both values; never expose these in frontend build-time variables.
AI_DEVELOPER_PASSWORD=
AI_DEVELOPER_TOKEN=
AI_DEVELOPER_TOKEN_TTL_MINUTES=60
```

The AI assistant does not expose provider, base URL, model, or API-key controls in the chat. It always uses the server-side values above. When both developer secrets are configured, an authorized developer can open **Settings → Developer Options**, unlock the section, test a temporary provider configuration, and apply it for the current browser session only. API keys are never stored in `localStorage`.

For a manual backend run, place these variables in `backend/.env` (the backend loads that file when started from `backend`). For Docker Compose, put the same variables in the project-root `.env`; the backend service receives them through `docker-compose.yml`. Restart the backend after changing environment values.

## Notes

- Works locally with SQLite by default
- Ollama is optional for non-AI features
- Sample seed data is included

## License

MIT
