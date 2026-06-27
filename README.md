# AI-Powered Academic Recommendation & Learning Assistant

An intelligent academic platform that helps students study efficiently by organizing educational resources and recommending relevant content using Machine Learning clustering.

## Architecture

```
├── frontend/          # React + TypeScript + TailwindCSS + Shadcn UI
├── backend/           # FastAPI + SQLAlchemy + Scikit-learn + NLTK
├── docker-compose.yml # PostgreSQL, Backend, Frontend, Ollama
├── .env.example       # Environment variables template
├── dataset/           # Academic dataset (user-provided)
├── uploads/           # Uploaded resources
└── docs/              # Documentation
```

## Tech Stack

| Layer      | Technology                                      |
|------------|------------------------------------------------|
| Frontend   | React, TypeScript, TailwindCSS, Shadcn UI, React Router, TanStack Query |
| Backend    | FastAPI, Python, SQLAlchemy, Pydantic          |
| Database   | PostgreSQL 16                                   |
| ML Engine  | Scikit-learn (TF-IDF + K-Means), NLTK          |
| AI         | Ollama (Qwen2.5 3B)                            |
| Deployment | Docker, Docker Compose                          |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

### Using Docker (Recommended)

```bash
# Clone and navigate to project
cd 0xCollage

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Seed the database with sample data
docker-compose exec backend python -m app.seed.seed_data

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
# Ollama: http://localhost:11434
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Set environment variables
export DATABASE_URL=postgresql://academic_user:academic_pass@localhost:5432/academic_db

# Run seed data
python -m app.seed.seed_data

# Start server
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Academic Data
| Method | Endpoint                        | Description                    |
|--------|--------------------------------|--------------------------------|
| GET    | /api/semesters                  | List all semesters             |
| GET    | /api/semesters/{id}             | Get semester with subjects     |
| GET    | /api/subjects                   | List all subjects              |
| GET    | /api/subjects/{id}              | Get subject with units         |
| GET    | /api/units/{id}                 | Get unit with topics           |
| GET    | /api/topics/{id}                | Get topic with resources       |
| GET    | /api/search?q=                  | Search subjects and topics     |

### Recommendations & AI
| Method | Endpoint                        | Description                    |
|--------|--------------------------------|--------------------------------|
| GET    | /api/recommendations/{topic_id} | Get similar topics (ML-based) |
| POST   | /api/ai/chat                    | Chat with AI assistant        |

### Faculty
| Method | Endpoint                        | Description                    |
|--------|--------------------------------|--------------------------------|
| POST   | /api/faculty/resources          | Add new resource (no auth v1) |

## ML Pipeline

```
Topic Text → Preprocessing (NLTK) → TF-IDF Vectorization → K-Means Clustering → Similar Topics
```

## Pages

- **Homepage** - Search bar, featured semesters, trending topics
- **Subjects** - All subjects with semester filter
- **Subject Detail** - Units overview with topic counts
- **Unit Page** - Topics list with importance scores
- **Topic Dashboard** - Resources (notes, videos, PYQs) + AI assistant panel
- **Search** - Full-text search results
- **Faculty** - Resource management form
- **Settings** - Configuration

## Environment Variables

| Variable         | Default                                        | Description          |
|------------------|------------------------------------------------|----------------------|
| POSTGRES_USER    | academic_user                                  | Database user        |
| POSTGRES_PASSWORD| academic_pass                                  | Database password    |
| POSTGRES_DB      | academic_db                                    | Database name        |
| DATABASE_URL     | postgresql://academic_user:academic_pass@postgres:5432/academic_db | Connection string |
| OLLAMA_BASE_URL  | http://ollama:11434                            | Ollama API URL       |
| OLLAMA_MODEL     | qwen2.5:3b                                     | LLM model            |
| VITE_API_URL     | http://localhost:8000                           | Backend API URL      |

## License

MIT
