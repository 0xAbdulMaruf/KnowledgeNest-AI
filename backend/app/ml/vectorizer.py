import logging

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer as SklearnTfidf

logger = logging.getLogger(__name__)

# Lazy-loaded dense embedding model — only imported when used.
_DENSE_MODEL = None
_DENSE_MODEL_NAME = "all-MiniLM-L6-v2"


def _get_dense_model():
    """Lazy-load the SentenceTransformer model (∼80 MB, only loaded once)."""
    global _DENSE_MODEL
    if _DENSE_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required for dense embeddings. "
                "Install it with: pip install sentence-transformers"
            ) from exc
        logger.info("Loading SentenceTransformer model: %s", _DENSE_MODEL_NAME)
        _DENSE_MODEL = SentenceTransformer(_DENSE_MODEL_NAME)
    return _DENSE_MODEL


class Vectorizer:
    """Text vectorizer supporting both TF-IDF (sparse/classic) and dense embeddings.

    Use ``method='tfidf'`` for the classic approach or ``method='dense'`` for
    semantic similarity via SentenceTransformer.
    """

    def __init__(self, max_features: int = 5000, method: str = "tfidf"):
        if method not in ("tfidf", "dense"):
            raise ValueError(f"Unknown vectorizer method: {method}. Use 'tfidf' or 'dense'.")
        self.method = method
        self._max_features = max_features
        self._vectorizer = SklearnTfidf(max_features=max_features) if method == "tfidf" else None
        self._fitted = False
        self._dimension: int | None = None

    def fit_transform(self, texts: list[str]) -> np.ndarray:
        self._fitted = True
        if self.method == "dense":
            model = _get_dense_model()
            vectors: np.ndarray = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
            self._dimension = vectors.shape[1]
            return vectors
        # TF-IDF path
        result = self._vectorizer.fit_transform(texts).toarray()  # type: ignore[union-attr]
        self._dimension = result.shape[1]
        return result

    def transform(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Vectorizer has not been fitted yet")
        if self.method == "dense":
            model = _get_dense_model()
            return model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return self._vectorizer.transform(texts).toarray()  # type: ignore[union-attr]

    @property
    def dimension(self) -> int | None:
        """Return the dimensionality of fitted vectors (or None if not fitted)."""
        return self._dimension

    @property
    def vocabulary(self) -> dict[str, int]:
        if self.method != "tfidf" or self._vectorizer is None:
            raise RuntimeError("Vocabulary is only available for TF-IDF vectorizers")
        return self._vectorizer.vocabulary_
