# 🤖 AI-Powered Academic Recommendation & Learning Assistant

> **Helping students find the right study material... because searching through 37 WhatsApp groups isn't an effective learning strategy.**

An AI-powered academic platform that organizes subjects, recommends related topics using Machine Learning, and provides an AI assistant to help students learn smarter—not harder.

> *Disclaimer:* It can recommend topics. It cannot recommend starting your assignment before the deadline.

---

## ✨ Features

* 📚 Organized academic hierarchy (Semester → Subject → Unit → Topic)
* 🔍 Fast search across topics and learning resources
* 🧠 ML-powered topic recommendations using TF-IDF + K-Means
* 🤖 AI study assistant powered by Ollama
* 📄 Support for notes, videos, and previous year questions
* 👨‍🏫 Faculty portal for uploading learning resources
* 🐳 Docker support for one-command deployment

---

## 🛠 Tech Stack

| Frontend           | Backend | Database   | ML                  | AI     |
| ------------------ | ------- | ---------- | ------------------- | ------ |
| React + TypeScript | FastAPI | PostgreSQL | Scikit-learn + NLTK | Ollama |

**Translation for non-developers:**

* React makes it look nice.
* FastAPI makes it fast.
* PostgreSQL remembers things.
* Scikit-learn finds similar topics.
* Ollama answers your questions without saying *"Read the documentation."*

---

## 🚀 Getting Started

```bash
git clone <repo-url>

cd 0xCollage

cp .env.example .env

docker-compose up -d

docker-compose exec backend python -m app.seed.seed_data
```

Then visit:

* 🌐 Frontend → `http://localhost:5173`
* 📚 API → `http://localhost:8000/docs`

If everything starts successfully on the first try...

...don't touch anything.

---

## 📖 Documentation

Want the boring (but useful) details?

* 📡 **API Documentation** → [`docs/API.md`](docs/API.md)
* 🏗️ **Project Structure** → [`docs/STRUCTURE.md`](docs/STRUCTURE.md)

---

## 💡 Why This Project?

Students waste too much time looking for notes, previous year questions, and relevant study resources.

This project brings everything into one place and uses Machine Learning to recommend related topics—so you spend less time searching and more time pretending you'll start studying tomorrow.

---

## 🤝 Contributing

Pull requests are always welcome.

Just remember:

> "99 little bugs in the code,
> 99 little bugs...
> Fix one bug,
> Commit the patch,
> 127 little bugs in the code."

---

## 📜 License

MIT License.

Use it.
Fork it.
Improve it.

Just don't name your notes folder:

```text
Notes/
├── Final/
├── Final_Final/
├── Final_Final_v2/
├── FINAL_REAL/
└── FINAL_REAL_THIS_ONE.pdf
```

We've all been there.

---

⭐ **If this project made your semester even 1% less painful, consider giving it a star.**

It won't improve your GPA...

...but it'll make the repository feel appreciated.
