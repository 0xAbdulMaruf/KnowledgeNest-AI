# AI-Powered Academic Recommendation & Learning Assistant

An intelligent academic platform that helps students study efficiently by organizing educational resources and recommending relevant content using Machine Learning clustering.

---

## Features

- **Academic Hierarchy**: Semester → Subject → Unit → Topic → Resources
- **ML Recommendations**: TF-IDF + K-Means clustering for similar topic suggestions
- **AI Assistant**: Context-aware study help powered by Ollama
- **Live Search**: Real-time search with relevance scoring
- **Resource Management**: Notes, videos, PYQs, coding problems, and more
- **Faculty Portal**: Upload and manage academic resources

---

## Tech Stack

| Layer      | Technology                                      |
|------------|------------------------------------------------|
| Frontend   | React, TypeScript, TailwindCSS, Shadcn UI      |
| Backend    | FastAPI, Python, SQLAlchemy, Pydantic          |
| Database   | SQLite (local development)                     |
| ML Engine  | Scikit-learn (TF-IDF + K-Means), NLTK          |
| AI         | Ollama (Qwen2.5 3B or configurable)            |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama (optional, for AI features)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Run seed scripts (creates SQLite database)
python -m app.seed.seed_c_python
python -m app.seed.seed_python_unit1
python -m app.seed.seed_python_unit2

# Start backend server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Project Structure

```
0xCollage/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── ml/           # ML recommendation engine
│   │   ├── llm/          # Ollama AI integration
│   │   └── seed/         # Database seed scripts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API client
│   │   └── lib/          # Utilities
│   └── package.json
├── FilesBYuser/          # User-provided files (syllabus, etc.)
└── README.md
```

---

## API Endpoints

### Academic Data

| Method | Endpoint                    | Description                    |
|--------|----------------------------|--------------------------------|
| GET    | /api/semesters              | List all semesters             |
| GET    | /api/subjects               | List all subjects              |
| GET    | /api/subjects/{id}          | Get subject with units         |
| GET    | /api/units/{id}             | Get unit with topics           |
| GET    | /api/topics/{id}            | Get topic with resources       |
| GET    | /api/search?q=              | Search subjects and topics     |

### Recommendations & AI

| Method | Endpoint                    | Description                    |
|--------|----------------------------|--------------------------------|
| GET    | /api/recommendations/{id}   | Get similar topics (ML-based)  |
| POST   | /api/ai/chat                | Chat with AI assistant         |

---

## ML Pipeline

```
Topic Text → Preprocessing (NLTK) → TF-IDF Vectorization → K-Means Clustering → Similar Topics
```

The recommendation engine analyzes topic descriptions and resource content to find semantically similar topics.

---

## Database

Using **SQLite** for local development. The database file is created automatically at `backend/academic_platform.db`.

### Seed Data

The project includes seed scripts for:
- **C Programming (CST201)**: 5 units, 22 topics
- **Python (CST203)**: 5 units, 16 topics
- **Detailed Unit 1**: 6 topics with GFG resources
- **Detailed Unit 2**: 3 topics with GFG resources

Run seed scripts:
```bash
python -m app.seed.seed_c_python
python -m app.seed.seed_python_unit1
python -m app.seed.seed_python_unit2
```

---

## Pages

- **Homepage**: Search bar, semester grid, quick access
- **Subjects**: All subjects with semester filter
- **Subject Detail**: Units overview with topic counts
- **Unit Page**: Topics list with importance scores
- **Topic Dashboard**: Resources + AI assistant
- **Search**: Live search with relevance scoring
- **Faculty**: Resource upload form
- **Settings**: Configuration

---

## Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./academic_platform.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
```

---

## License

MIT License
