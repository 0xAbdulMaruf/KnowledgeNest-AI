# 📡 API Documentation

Welcome to the API docs.

If you're here because the frontend exploded, welcome.
If you're here because you like reading APIs for fun... we have questions.

---

# 🌐 Base URL

```text
http://localhost:8000
```

Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

Because life's too short to manually test every endpoint with `curl`.

---

# 🔐 Authentication

**Current Status:** None (v1)

Yes, we know.

No, don't expose this directly to the internet.

Authentication is planned for a future release—right after we finish saying *"we'll add it later."*

---

# 📚 Academic Endpoints

These endpoints power the core academic hierarchy.

```
Semester
   └── Subject
        └── Unit
             └── Topic
```

Basically... a fancy tree that eventually leads to exam anxiety.

---

## Semesters

| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| GET    | `/api/semesters`      | List all semesters         |
| GET    | `/api/semesters/{id}` | Get semester with subjects |

---

## Subjects

| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| GET    | `/api/subjects`      | List all subjects          |
| GET    | `/api/subjects/{id}` | Subject details with units |

---

## Units

| Method | Endpoint          | Description      |
| ------ | ----------------- | ---------------- |
| GET    | `/api/units/{id}` | Unit with topics |

---

## Topics

| Method | Endpoint           | Description                        |
| ------ | ------------------ | ---------------------------------- |
| GET    | `/api/topics/{id}` | Topic details & learning resources |

---

## Search

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/search?q=` | Search subjects and topics |

Example:

```http
GET /api/search?q=operating systems
```

Finally...

A search engine that doesn't return Stack Overflow answers from 2009.

---

# 🤖 AI Endpoints

Because every project gets +10 cool points once you add "AI".

---

## Chat Assistant

| Method | Endpoint       |
| ------ | -------------- |
| POST   | `/api/ai/chat` |

Send a prompt to the local LLM.

Example:

```json
{
  "message": "Explain deadlocks like I'm five."
}
```

Expected outcome:

* ✅ Explains deadlocks.
* ❌ Doesn't do your assignment.

---

# 🧠 Recommendation Engine

Machine Learning powered topic recommendations.

| Method | Endpoint                          |
| ------ | --------------------------------- |
| GET    | `/api/recommendations/{topic_id}` |

Pipeline:

```text
Topic
   │
   ▼
NLTK Cleaning
   │
   ▼
TF-IDF
   │
   ▼
K-Means
   │
   ▼
Similar Topics
```

Translation:

> "If you're studying Binary Trees, maybe Graphs are about to become your next problem."

---

# 👨‍🏫 Faculty Endpoints

Currently available:

| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| POST   | `/api/faculty/resources` | Upload learning resources |

Authentication?

Not yet.

Please behave.

---

# 📦 Response Format

Successful responses generally look like:

```json
{
  "success": true,
  "data": { }
}
```

Errors usually look like:

```json
{
  "detail": "Something went wrong."
}
```

If you receive:

```json
{
  "detail": "Internal Server Error"
}
```

Congratulations.

You've discovered a bug before we did.

---

# 🧪 Testing

The easiest way to test the API:

1. Start the backend.
2. Open `/docs`.
3. Click an endpoint.
4. Press **Try it out**.
5. Feel like a hacker.

No complicated setup required.

---

# ⚠️ Notes

* Responses are JSON.
* IDs are integer-based.
* The API is RESTful.
* The AI occasionally hallucinates.
* Your professor occasionally does too.

Always verify important information.

---

# 🐛 Common Problems

### 404 Not Found

You're asking for something that doesn't exist.

Much like your motivation the night before exams.

---

### 500 Internal Server Error

Something exploded.

Please open an issue...

...after making sure it wasn't your fault first. 😄

---

