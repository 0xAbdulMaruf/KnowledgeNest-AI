import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer as SklearnTfidf


class Vectorizer:
    def __init__(self, max_features: int = 5000):
        self._vectorizer = SklearnTfidf(max_features=max_features)
        self._fitted = False

    def fit_transform(self, texts: list[str]) -> np.ndarray:
        self._fitted = True
        return self._vectorizer.fit_transform(texts).toarray()

    def transform(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Vectorizer has not been fitted yet")
        return self._vectorizer.transform(texts).toarray()

    @property
    def vocabulary(self) -> dict[str, int]:
        return self._vectorizer.vocabulary_
