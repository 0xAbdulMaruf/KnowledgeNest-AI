import os
import json
import pickle
from pathlib import Path

import numpy as np

from app.ml.preprocessing import preprocess_text
from app.ml.vectorizer import Vectorizer
from app.ml.clustering import Clusterer

MODEL_DIR = Path(os.getenv("ML_MODEL_DIR", "/tmp/academic_ml_models"))


class Recommender:
    def __init__(self, n_clusters: int = 10):
        self.vectorizer = Vectorizer()
        self.clusterer = Clusterer(n_clusters=n_clusters)
        self.topic_ids: list[int] = []
        self.topic_vectors: np.ndarray | None = None
        self._fitted = False

    def fit(self, topics: list) -> None:
        self.topic_ids = [t.id for t in topics]
        texts = []
        for t in topics:
            raw = f"{t.name} {t.description or ''} {' '.join(t.tags or [])}"
            texts.append(preprocess_text(raw))

        self.topic_vectors = self.vectorizer.fit_transform(texts)
        n_clusters = min(len(topics), self.clusterer._kmeans.n_clusters)
        if n_clusters < 2:
            n_clusters = 2
        self.clusterer = Clusterer(n_clusters=n_clusters)
        self.clusterer.fit(self.topic_vectors)
        self._fitted = True

    def _calculate_similarity(self, topic_id: int) -> list[tuple[int, float]]:
        """Calculate similarity scores for all topics relative to the given topic."""
        if not self._fitted or self.topic_vectors is None:
            return []

        if topic_id not in self.topic_ids:
            return []

        idx = self.topic_ids.index(topic_id)
        target_vector = self.topic_vectors[idx]
        target_cluster = self.clusterer.predict(target_vector.reshape(1, -1))[0]
        all_clusters = self.clusterer.labels

        similarities = []
        for i, tid in enumerate(self.topic_ids):
            if tid == topic_id:
                continue
            vec = self.topic_vectors[i]
            dot = np.dot(target_vector, vec)
            norm = np.linalg.norm(target_vector) * np.linalg.norm(vec)
            cosine = dot / norm if norm > 0 else 0.0
            cluster_bonus = 0.3 if all_clusters[i] == target_cluster else 0.0
            score = cosine + cluster_bonus
            # Normalize score to 0-1 range
            normalized_score = min(max(score / 1.3, 0.0), 1.0)
            similarities.append((tid, normalized_score))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def find_similar_topics(self, topic_id: int, top_k: int = 5) -> list[int]:
        similarities = self._calculate_similarity(topic_id)
        return [tid for tid, _ in similarities[:top_k]]

    def find_similar_topics_with_scores(self, topic_id: int, top_k: int = 5) -> list[tuple[int, float]]:
        similarities = self._calculate_similarity(topic_id)
        return similarities[:top_k]

    def save(self, path: Path | None = None) -> None:
        save_dir = path or MODEL_DIR
        save_dir.mkdir(parents=True, exist_ok=True)
        with open(save_dir / "recommender.pkl", "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: Path | None = None) -> "Recommender":
        load_dir = path or MODEL_DIR
        filepath = load_dir / "recommender.pkl"
        if not filepath.exists():
            return cls()
        with open(filepath, "rb") as f:
            return pickle.load(f)
