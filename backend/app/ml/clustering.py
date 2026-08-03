import numpy as np
from sklearn.cluster import KMeans


class Clusterer:
    def __init__(self, n_clusters: int = 10, random_state: int = 42):
        self._n_clusters = n_clusters
        self._random_state = random_state
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self._fitted = False

    def fit(self, X: np.ndarray) -> None:
        # Ensure n_clusters doesn't exceed number of samples
        n_samples = X.shape[0]
        if self._n_clusters > n_samples:
            self._n_clusters = max(2, n_samples)
            self._kmeans = KMeans(n_clusters=self._n_clusters, random_state=self._random_state, n_init=10)
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

    @property
    def inertia(self) -> float:
        """Sum of squared distances to closest centroid (lower = tighter clusters)."""
        return float(self._kmeans.inertia_)
