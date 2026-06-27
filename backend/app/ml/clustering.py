import numpy as np
from sklearn.cluster import KMeans


class Clusterer:
    def __init__(self, n_clusters: int = 10, random_state: int = 42):
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self._fitted = False

    def fit(self, X: np.ndarray) -> None:
        self._kmeans.fit(X)
        self._fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Clusterer has not been fitted yet")
        return self._kmeans.predict(X)

    @property
    def cluster_centers(self) -> np.ndarray:
        return self._kmeans.cluster_centers_

    @property
    def labels(self) -> np.ndarray:
        return self._kmeans.labels_
