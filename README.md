# 📚 KnowledgeNest AI

> *"Because copy-pasting from StackOverflow isn't a learning strategy... or is it?" 😄*

An **AI-powered academic companion** that turns the chaotic mess of your syllabus, notes, and past exam papers into an actually organized learning experience. Think of it as having a really smart study buddy who never gets tired of explaining things.

---

## ✨ What Makes Us Different?

-  **Smart Academic Hierarchy**: Semester → Subject → Unit → Topic → Resources (Finally, some structure!)
-  **ML Recommendations**: TF-IDF + K-Means clustering that actually understands what you're studying
-  **AI Study Assistant**: Ollama-powered, context-aware help that doesn't judge your 2 AM study sessions
-  **Live Search**: Find that one resource you remember seeing *somewhere* without losing your mind
-  **Resource Hub**: Notes, videos, PYQs, coding problems, and more — all in one place
-  **Faculty Portal**: Teachers can upload resources (finally, an organized way!)

---

## 🛠️ Tech Stack

Built with the best tools so you don't have to deal with technical debt as a student:

| Layer          | Technology                                 | Why? |
|----------------|-------------------------------------------|------|
| **Frontend**   | React + TypeScript + TailwindCSS + Shadcn | Type safety is our love language |
| **Backend**    | FastAPI + Python + SQLAlchemy + Pydantic | Fast, scalable, Pythonic ✨ |
| **Database**   | SQLite (dev) / Upgradeable to PostgreSQL  | Lightweight, works offline |
| **ML Engine**  | Scikit-learn (TF-IDF + K-Means) + NLTK   | Smart recommendations for smart students |
| **AI Brain**   | Ollama (Qwen2.5 3B, customizable)        | Runs locally, respects your privacy |

---

##  Quick Start (Copy-Paste Edition)

### Prerequisites

```bash
✓ Python 3.11
✓ Node.js 18+
✓ Ollama (optional, but recommended — don't miss out on AI magic!)
✓ A functioning keyboard (preferred)
```

### Backend Setup

```bash
# Navigate to backend (let's get this party started)
cd backend

# Create a virtual environment (keep things isolated)
python -m venv venv
source venv/bin/activate  # Windows users: venv\Scripts\activate

# Install dependencies (this might take a minute...)
pip install -r requirements.txt

# Download NLTK data (natural language magic incoming)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Seed the database with some sample data
python -m app.seed.seed_c_python
python -m app.seed.seed_python_unit1
python -m app.seed.seed_python_unit2

# Start the backend (uvicorn is fast AF)
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend (where the pretty stuff happens)
cd frontend

# Install dependencies
npm install

# Start the dev server (hot reload ftw!)
npm run dev
```

###  Access Points

| What | Where |
|------|-------|
| **Your App** | http://localhost:5173 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs *(Swagger — beautiful!)* |

---

## 📁 Project Structure

```
KnowledgeNest-AI/
├── backend/                    # Python FastAPI magic
│   ├── app/
│   │   ├── api/               # All the endpoints you'll ever need
│   │   ├── models/            # Database models (SQLAlchemy wizardry)
│   │   ├── schemas/           # Data validation (Pydantic > bugs)
│   │   ├── services/          # Business logic (the brains)
│   │   ├── ml/                # ML recommendation engine (the smart part)
│   │   ├── llm/               # Ollama AI integration (the brilliant part)
│   │   └── seed/              # Database seeding (initial data)
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React TypeScript beauty
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/             # Page-level components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API calls & external services
│   │   └── lib/               # Utilities & helpers
│   └── package.json
│
├── FilesByUser/               # User uploads (organized chaos)
└── README.md                  # You are here 👈
```

---

##  API Endpoints

###  Academic Data Endpoints

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| GET | `/api/semesters` | List all semesters |
| GET | `/api/subjects` | Browse all subjects |
| GET | `/api/subjects/{id}` | Dive into a specific subject |
| GET | `/api/units/{id}` | Explore units within a subject |
| GET | `/api/topics/{id}` | See topics with resources |
| GET | `/api/search?q=keyword` | Find anything (seriously, try it!) |

###  Recommendations & AI Endpoints

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| GET | `/api/recommendations/{id}` | Get similar topics (ML magic) |
| POST | `/api/ai/chat` | Chat with the AI assistant |

---

##  How the ML Magic Works

```
Your Topic
    ↓
NLTK Preprocessing (cleaning up the mess)
    ↓
TF-IDF Vectorization (converting to numbers)
    ↓
K-Means Clustering (finding friends)
    ↓
Similar Topics 🎯
```

**In simple terms**: We analyze what you're learning and suggest related topics you might find helpful. No magic wand needed, just math. 📐

---

##  Database

**SQLite** for local development (zero setup!). Database file lives at `backend/academic_platform.db`.

### Built-in Sample Data

We include seed scripts with real course data:
- **C Programming (CST201)**: 5 units, 22 topics
- **Python (CST203)**: 5 units, 16 topics  
- **Detailed Units**: Complete with GeeksforGeeks resources

Run them all at once:
```bash
python -m app.seed.seed_c_python && python -m app.seed.seed_python_unit1 && python -m app.seed.seed_python_unit2
```

---

## 📱 Pages & Features

| Page | What You Can Do |
|------|-----------------|
| ** Homepage** | Search, explore semesters, jump to favorites |
| ** Subjects** | Browse all subjects (filtered by semester) |
| ** Subject Detail** | See all units with topic counts |
| ** Unit Page** | Browse topics with importance scores |
| ** Topic Dashboard** | Access resources + chat with AI |
| ** Search** | Live search with relevance scoring (powered by ML) |
| ** Faculty Portal** | Upload and manage resources |
| ** Settings** | Customize your experience |

---

##  Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database connection
DATABASE_URL=sqlite:///./academic_platform.db

# Ollama AI configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b

# Add more as needed!
```

---

##  Contributing

Found a bug? Have an idea? We'd love your help!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License — Use it, modify it, make it yours! 🚀

---

##  Pro Tips

- **Offline learning**: Run everything locally. No internet? No problem!
- **Customize the AI**: Change the Ollama model in `.env` for different behavior
- **Seed your own data**: Follow the seed script pattern to add your courses
- **Production ready**: Upgrade to PostgreSQL when you're scaling up

---

## 🤔 FAQ

**Q: Can I use this without Ollama?**  
A: Yes! The AI features are optional. Everything else works great.

**Q: Is this only for CS students?**  
A: Nope! Any academic subject works — just seed the database with your courses.

**Q: Will this make me smarter?**  
A: It'll definitely make your studying smarter. Personal smarts are on you! 😄

---

**Made with ❤️ by students, for students.**

*P.S. — If this helps you ace your exams, remember to share it with your classmates. Sharing is caring! 📚*
