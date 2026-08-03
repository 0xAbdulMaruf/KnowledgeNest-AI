import json
import logging
import os
import pickle
from pathlib import Path
from typing import Sequence

import numpy as np

from app.ml.preprocessing import preprocess_text
from app.ml.vectorizer import Vectorizer
from app.ml.clustering import Clusterer

logger = logging.getLogger(__name__)

MODEL_DIR = Path(os.getenv("ML_MODEL_DIR", "/tmp/academic_ml_models"))
VECTOR_METHOD = os.getenv("ML_VECTOR_METHOD", "tfidf")  # "tfidf" or "dense"

# ── Multi-signal scoring weights ──────────────────────────
SIGNAL_WEIGHTS: dict[str, float] = {
    "text_similarity": 0.45,       # Cosine / dot-product similarity of topic vectors
    "tag_overlap": 0.20,           # Jaccard similarity of tag sets
    "same_unit": 0.12,             # Bonus when topics share the same unit
    "same_subject": 0.08,          # Bonus when topics share the same subject
    "importance_alignment": 0.10,  # Bonus when importance scores are close
    "resource_overlap": 0.05,      # Bonus when resource types overlap
}


class Recommender:
    def __init__(self, n_clusters: int = 10, vector_method: str | None = None):
        method = vector_method or VECTOR_METHOD
        self.vectorizer = Vectorizer(method=method)
        self.clusterer = Clusterer(n_clusters=n_clusters)
        self.topic_ids: list[int] = []
        self.topic_vectors: np.ndarray | None = None
        # Store metadata per topic for multi-signal scoring
        self._topic_meta: dict[int, dict] = {}
        self._fitted = False

    # ── Public API ────────────────────────────────────────

    def fit(self, topics: Sequence) -> None:
        """Fit the recommender on a list of Topic-like objects.

        Each topic must have: id, name, description, tags, unit_id.
        Optionally: unit.subject_id, importance_score, resources.
        """
        self.topic_ids = [t.id for t in topics]
        texts = []
        self._topic_meta = {}

        for t in topics:
            # Build rich text from topic + its resources
            parts = [t.name, t.description or "", " ".join(t.tags or [])]

            # Append resource content for richer semantics
            if hasattr(t, "resources") and t.resources:
                resource_texts = []
                resource_types: set[str] = set()
                for resource in t.resources:
                    if getattr(resource, "deleted_at", None) is not None:
                        continue
                    if resource.content:
                        resource_texts.append(resource.content[:800])
                    resource_types.add(getattr(resource.type, "value", str(resource.type)))
                if resource_texts:
                    parts.append(" ".join(resource_texts))

            raw = " ".join(parts)
            texts.append(preprocess_text(raw))

            # Store metadata for multi-signal scoring
            self._topic_meta[t.id] = {
                "name": t.name,
                "tags": set(t.tags or []),
                "unit_id": t.unit_id,
                "subject_id": getattr(t.unit, "subject_id", None) if hasattr(t, "unit") and t.unit else None,
                "importance_score": getattr(t, "importance_score", None) or 0.0,
                "resource_types": (
                    {getattr(r.type, "value", str(r.type)) for r in t.resources
                     if getattr(r, "deleted_at", None) is None}
                    if hasattr(t, "resources") and t.resources else set()
                ),
            }

        self.topic_vectors = self.vectorizer.fit_transform(texts)
        n_clusters = min(len(topics), self.clusterer._kmeans.n_clusters)
        if n_clusters < 2:
            n_clusters = 2
        self.clusterer = Clusterer(n_clusters=n_clusters)
        self.clusterer.fit(self.topic_vectors)
        self._fitted = True
        logger.info("Recommender fitted on %d topics (method=%s, clusters=%d)", len(topics), self.vectorizer.method, n_clusters)

    # ── Scoring ───────────────────────────────────────────

    def _compute_similarity(self, topic_id: int) -> list[tuple[int, float, dict[str, float]]]:
        """Compute similarity with multi-signal scoring.

        Returns list of (topic_id, total_score, signal_breakdown) sorted descending.
        """
        if not self._fitted or self.topic_vectors is None:
            return []

        if topic_id not in self.topic_ids:
            return []

        idx = self.topic_ids.index(topic_id)
        target_vector = self.topic_vectors[idx]
        target_meta = self._topic_meta.get(topic_id, {})

        results: list[tuple[int, float, dict[str, float]]] = []

        for i, other_id in enumerate(self.topic_ids):
            if other_id == topic_id:
                continue

            other_vector = self.topic_vectors[i]
            other_meta = self._topic_meta.get(other_id, {})

            signals = self._compute_signals(target_vector, other_vector, target_meta, other_meta)
            total = sum(signals[signal] * SIGNAL_WEIGHTS.get(signal, 0.0) for signal in signals)
            # Clamp to [0, 1]
            total = max(0.0, min(total, 1.0))
            results.append((other_id, total, signals))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _compute_signals(
        self,
        vec_a: np.ndarray,
        vec_b: np.ndarray,
        meta_a: dict,
        meta_b: dict,
    ) -> dict[str, float]:
        """Compute all similarity signals between two topics."""
        signals: dict[str, float] = {}

        # 1. Text similarity (cosine)
        dot = float(np.dot(vec_a, vec_b))
        norm = float(np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        signals["text_similarity"] = (dot / norm) if norm > 0 else 0.0

        # 2. Tag Jaccard overlap
        tags_a = meta_a.get("tags", set())
        tags_b = meta_b.get("tags", set())
        if tags_a or tags_b:
            intersection = len(tags_a & tags_b)
            union = len(tags_a | tags_b)
            signals["tag_overlap"] = intersection / union if union > 0 else 0.0
        else:
            signals["tag_overlap"] = 0.0

        # 3. Same-unit bonus
        signals["same_unit"] = 1.0 if meta_a.get("unit_id") == meta_b.get("unit_id") else 0.0

        # 4. Same-subject bonus
        signals["same_subject"] = (
            1.0
            if meta_a.get("subject_id") is not None
            and meta_a.get("subject_id") == meta_b.get("subject_id")
            else 0.0
        )

        # 5. Importance alignment (closer scores = higher signal)
        imp_a = float(meta_a.get("importance_score", 0))
        imp_b = float(meta_b.get("importance_score", 0))
        signals["importance_alignment"] = 1.0 - min(abs(imp_a - imp_b), 1.0)

        # 6. Resource type overlap
        res_a = meta_a.get("resource_types", set())
        res_b = meta_b.get("resource_types", set())
        if res_a or res_b:
            intersection = len(res_a & res_b)
            union = len(res_a | res_b)
            signals["resource_overlap"] = intersection / union if union > 0 else 0.0
        else:
            signals["resource_overlap"] = 0.0

        return signals

    def _top_signal_label(self, signals: dict[str, float]) -> str:
        """Return a human-readable label for the dominant signal."""
        labels = {
            "text_similarity": "Similar content",
            "tag_overlap": "Shared tags",
            "same_unit": "Same unit",
            "same_subject": "Same subject",
            "importance_alignment": "Similar importance",
            "resource_overlap": "Similar resources",
        }
        # Find the signal with the highest weighted contribution
        best_signal = max(
            signals,
            key=lambda s: signals[s] * SIGNAL_WEIGHTS.get(s, 0.0),
        )
        return labels.get(best_signal, "Related content")

    # ── Query methods ─────────────────────────────────────

    def find_similar_topics(self, topic_id: int, top_k: int = 5) -> list[int]:
        results = self._compute_similarity(topic_id)
        return [tid for tid, _, _ in results[:top_k]]

    def find_similar_topics_with_scores(self, topic_id: int, top_k: int = 5) -> list[tuple[int, float]]:
        results = self._compute_similarity(topic_id)
        return [(tid, score) for tid, score, _ in results[:top_k]]

    def find_similar_topics_with_signals(self, topic_id: int, top_k: int = 5) -> list[tuple[int, float, dict[str, float], str]]:
        """Return top-k similar topics with score, signal breakdown, and dominant reason."""
        results = self._compute_similarity(topic_id)
        return [
            (tid, score, signals, self._top_signal_label(signals))
            for tid, score, signals in results[:top_k]
        ]

    # ── Persistence ───────────────────────────────────────

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
        try:
            with open(filepath, "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError, ModuleNotFoundError) as exc:
            logger.warning("Failed to load recommender model, creating new one: %s", exc)
            return cls()
