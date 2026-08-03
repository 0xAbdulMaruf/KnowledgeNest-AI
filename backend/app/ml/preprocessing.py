import functools
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def _ensure_nltk_data() -> None:
    """Download required NLTK data once at module load."""
    for resource, name in [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
    ]:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(name, quiet=True)


_ensure_nltk_data()


@functools.lru_cache(maxsize=512)
def _preprocess_cached(text: str) -> str:
    """Cached text preprocessing — useful when the same topic text is processed repeatedly."""
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)


def preprocess_text(text: str) -> str:
    """Preprocess text: lowercase, strip non-alpha, tokenize, remove stopwords, lemmatize."""
    return _preprocess_cached(text)
