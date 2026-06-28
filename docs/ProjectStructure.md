# 🏗️ Project Structure

> **"Where is the file I'm looking for?"**
> Hopefully this document answers that before you start using `find . -name "*whatever*"`.

This project is split into two main parts:

* 🎨 **Frontend** — Everything users see.
* ⚙️ **Backend** — Everything users don't see... unless it crashes.

---

# 📂 Root Directory

```text
.
├── frontend/              # React application
├── backend/               # FastAPI server
├── dataset/               # Academic dataset
├── uploads/               # Uploaded resources
├── docs/                  # Documentation
├── docker-compose.yml     # The "please just work" button
├── .env.example           # Environment template
└── README.md              # You're probably reading this already
```

---

# 🎨 Frontend

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── hooks/
│   ├── services/
│   ├── lib/
│   ├── assets/
│   └── App.tsx
└── package.json
```

## 📁 components/

Reusable UI components.

Buttons.

Cards.

Modals.

That one component everyone is afraid to modify because *"it somehow fixes three unrelated bugs."*

---

## 📄 pages/

Application pages.

Examples:

* Home
* Subjects
* Topic Dashboard
* Faculty Portal
* Search

If users can navigate to it...

...it probably lives here.

---

## 🎣 hooks/

Custom React hooks.

Because copying the same logic five times builds regret, not software.

---

## 🌐 services/

Handles API requests.

The frontend politely asks.

The backend politely responds.

Sometimes.

---

## 📚 lib/

Shared utilities and helper functions.

A fancy name for *"functions we got tired of rewriting."*

---

# ⚙️ Backend

```text
backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── ml/
│   ├── seed/
│   ├── database.py
│   └── main.py
├── requirements.txt
└── Dockerfile
```

---

## 🌐 api/

Defines API routes.

Every request starts here.

It's basically the receptionist of the backend.

---

## 🗄️ models/

SQLAlchemy database models.

Think of these as the database's way of saying:

> "I'm just a bunch of tables wearing Python clothes."

---

## 📦 schemas/

Pydantic request and response models.

Keeps data clean.

Keeps developers sane.

Usually.

---

## 🛠️ services/

Business logic.

The API says:

> "User wants recommendations."

The service says:

> "Leave it to me."

---

## 🧠 ml/

Machine Learning logic.

Contains:

* Text preprocessing
* TF-IDF vectorization
* K-Means clustering
* Recommendation engine

In other words...

The folder with the smartest code in the repository.

---

## 🌱 seed/

Initial database population.

Useful when the database is emptier than your wallet after buying another programming course.

---

## 🚀 main.py

Application entry point.

If this file doesn't run...

Neither does anything else.

No pressure.

---

# 📂 Dataset

```text
dataset/
```

Contains the academic dataset used to populate the system.

Please upload course data.

Not your Spotify playlist.

---

# 📁 Uploads

```text
uploads/
```

Stores uploaded learning resources.

Expected content:

* 📄 Notes
* 📺 Videos
* 📝 Previous Year Questions
* 📚 PDFs

Unexpected content:

* `assignment_final_final_REAL.pdf`
* Family vacation photos
* Linux ISOs (tempting, but no)

---

# 🐳 Docker

```text
docker-compose.yml
```

Starts:

* PostgreSQL
* Backend
* Frontend
* Ollama

One command.

Four containers.

Countless dependency headaches avoided.

---

# 🔄 High-Level Flow

```text
            Student
               │
               ▼
        React Frontend
               │
         HTTP Requests
               │
               ▼
         FastAPI Backend
        ┌──────────────┐
        │              │
        ▼              ▼
 PostgreSQL      ML Engine
        │              │
        └──────┬───────┘
               ▼
          JSON Response
               │
               ▼
          Happy Student*
```

* Happiness during exam season is not guaranteed.

---

# 💡 Where Should I Add New Code?

| Want to...              | Go to...                   |
| ----------------------- | -------------------------- |
| Add a page              | `frontend/src/pages/`      |
| Create a UI component   | `frontend/src/components/` |
| Call a new API          | `frontend/src/services/`   |
| Add an endpoint         | `backend/app/api/`         |
| Add database tables     | `backend/app/models/`      |
| Add validation          | `backend/app/schemas/`     |
| Write business logic    | `backend/app/services/`    |
| Improve recommendations | `backend/app/ml/`          |

---

# 🎯 Final Advice

If you're looking for a file and can't find it:

1. Check this document.
2. Use your IDE's search.
3. Ask Git.
4. Panic.
5. Realize the file was open in another tab the whole time.

Welcome to software development. 🚀
