import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def preprocess_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)

    try:
        tokens = word_tokenize(text)
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        tokens = word_tokenize(text)

    try:
        stop_words = set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        stop_words = set(stopwords.words("english"))

    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

    try:
        lemmatizer = WordNetLemmatizer()
    except LookupError:
        nltk.download("wordnet", quiet=True)
        lemmatizer = WordNetLemmatizer()

    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)
