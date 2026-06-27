PROMPT_TEMPLATES: dict[str, dict[str, str]] = {
    "explain_topic": {
        "system": "You are an expert academic tutor. Explain concepts clearly with examples.",
        "template": "Explain the following academic topic in detail:\n\n{context}\n\nProvide a clear, structured explanation suitable for a college student.",
    },
    "generate_quiz": {
        "system": "You are an academic quiz generator. Create challenging but fair questions.",
        "template": "Based on this topic, generate a quiz with 5 questions and answers:\n\n{context}\n\nFormat each question with its answer.",
    },
    "answer_question": {
        "system": "You are a knowledgeable academic assistant. Answer questions accurately and helpfully.",
        "template": "Given the following topic context, answer the student's question:\n\nContext:\n{context}\n\nQuestion: {question}",
    },
    "generate_mcq": {
        "system": "You are an MCQ generator. Create multiple choice questions with 4 options each, marking the correct answer.",
        "template": "Based on this topic, generate 5 multiple-choice questions with 4 options each. Mark the correct answer.\n\n{context}\n\nFormat: Q: ...\nA) ...\nB) ...\nC) ...\nD) ...\nCorrect: X",
    },
}
