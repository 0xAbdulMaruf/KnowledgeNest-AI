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
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
```

## Notes

- Works locally with SQLite by default
- Ollama is optional for non-AI features
- Sample seed data is included

## License

MIT
