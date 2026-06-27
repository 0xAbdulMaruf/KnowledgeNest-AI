from app.ml.recommender import Recommender


class RecommendationService:
    def __init__(self):
        self._recommender: Recommender | None = None

    def _get_recommender(self) -> Recommender:
        if self._recommender is None:
            self._recommender = Recommender.load()
        return self._recommender

    def fit(self, topics: list) -> None:
        self._recommender = Recommender()
        self._recommender.fit(topics)
        self._recommender.save()

    def find_similar_topics(self, topic_id: int, all_topics: list, top_k: int = 5) -> list[int]:
        # Refit from the live topic table so cached models on disk cannot drift
        # out of sync with the current dataset.
        self.fit(all_topics)
        recommender = self._get_recommender()
        return recommender.find_similar_topics(topic_id, top_k=top_k)

    def find_similar_topics_with_scores(self, topic_id: int, all_topics: list, top_k: int = 5) -> list[tuple[int, float]]:
        # Refit from the live topic table so cached models on disk cannot drift
        # out of sync with the current dataset.
        self.fit(all_topics)
        recommender = self._get_recommender()
        return recommender.find_similar_topics_with_scores(topic_id, top_k=top_k)
