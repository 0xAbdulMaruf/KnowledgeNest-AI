import fcntl
import logging
import os
from pathlib import Path

from app.ml.recommender import Recommender, MODEL_DIR

logger = logging.getLogger(__name__)


class RecommendationService:
    """Thread- and worker-safe recommendation service.

    Uses file locking for pickle persistence and a content-aware fingerprint
    so the model refits when topic metadata, tags, or resources change.
    """

    def __init__(self):
        self._recommender: Recommender | None = None
        self._topic_fingerprint: int | None = None
        self._lock_path = Path(os.getenv("ML_LOCK_DIR", "/tmp")) / "recommender.lock"

    @staticmethod
    def _compute_fingerprint(topics: list) -> int:
        """Compute a hash that captures all recommendation-relevant topic state.

        Includes: IDs, names, descriptions, tags, importance scores, unit IDs,
        subject IDs, and resource types/content hashes.
        """
        items: list[tuple] = []
        for t in topics:
            unit = getattr(t, "unit", None)
            subject_id = getattr(unit, "subject_id", None) if unit else None

            resource_keys: list[tuple] = []
            if hasattr(t, "resources") and t.resources:
                for r in t.resources:
                    if getattr(r, "deleted_at", None) is not None:
                        continue
                    resource_keys.append((
                        getattr(r.type, "value", str(r.type)),
                        hash((r.content or "")[:200]) if r.content else 0,
                    ))

            items.append((
                t.id,
                t.name,
                (t.description or "")[:500],
                tuple(sorted(t.tags or [])),
                t.importance_score or 0.0,
                t.unit_id,
                subject_id,
                tuple(sorted(resource_keys)),
            ))
        return hash(tuple(sorted(items)))

    def _get_recommender(self) -> Recommender:
        if self._recommender is None:
            self._recommender = Recommender.load()
        return self._recommender

    def _acquire_lock(self) -> int:
        """Acquire an exclusive file lock. Returns the file descriptor."""
        fd = os.open(self._lock_path, os.O_CREAT | os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX)
        return fd

    @staticmethod
    def _release_lock(fd: int) -> None:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            pass
        try:
            os.close(fd)
        except OSError:
            pass

    def fit(self, topics: list) -> None:
        fd = self._acquire_lock()
        try:
            self._recommender = Recommender()
            self._recommender.fit(topics)
            self._recommender.save()
            self._topic_fingerprint = self._compute_fingerprint(topics)
            logger.info("Recommender fitted and saved (fingerprint=%s)", self._topic_fingerprint)
        finally:
            self._release_lock(fd)

    def _ensure_fitted(self, all_topics: list) -> None:
        """Refit only when the topic set has actually changed."""
        fingerprint = self._compute_fingerprint(all_topics)
        if self._topic_fingerprint != fingerprint or self._recommender is None:
            logger.info(
                "Refitting recommender — fingerprint changed from %s to %s",
                self._topic_fingerprint,
                fingerprint,
            )
            self.fit(all_topics)

    def find_similar_topics(self, topic_id: int, all_topics: list, top_k: int = 5) -> list[int]:
        self._ensure_fitted(all_topics)
        recommender = self._get_recommender()
        return recommender.find_similar_topics(topic_id, top_k=top_k)

    def find_similar_topics_with_scores(self, topic_id: int, all_topics: list, top_k: int = 5) -> list[tuple[int, float]]:
        self._ensure_fitted(all_topics)
        recommender = self._get_recommender()
        return recommender.find_similar_topics_with_scores(topic_id, top_k=top_k)

    def find_similar_topics_with_signals(
        self, topic_id: int, all_topics: list, top_k: int = 5
    ) -> list[tuple[int, float, dict[str, float], str]]:
        """Return recommendations with multi-signal breakdowns and dominant reason."""
        self._ensure_fitted(all_topics)
        recommender = self._get_recommender()
        return recommender.find_similar_topics_with_signals(topic_id, top_k=top_k)
