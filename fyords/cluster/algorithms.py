import random
import numpy as np

class KMeans:
    def __init__(self, x, y, k=8):
        self.X = list(zip(x, y))
        self.k = k
        self.centroids = self.get_centroids()

    @staticmethod
    def get_dist(a, b, axis=1):
        return np.linalg.norm(a-b, axis=axis)

    def to_dict(self):
        return {
            'X len': len(self.X),
            'k': self.k,
            'n centroids': len(self.centroids)
        }

    def get_k(self):
        """TODO: use elbow method to determin k"""
        pass

    def get_centroids(self):
        """get centroids using instance data"""
        c_x = np.random.randint(np.min(self.X), np.max(self.X), size=self.k)
        c_y = np.random.randint(np.min(self.X), np.max(self.X), size=self.k)
        return np.array(list(zip(c_x, c_y)), dtype=np.float32)
