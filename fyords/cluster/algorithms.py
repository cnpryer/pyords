from copy import deepcopy
import random
import numpy as np
import logging


class KMeans:
    def __init__(self, k=8):
        self.k = k

    @staticmethod
    def get_dist(a, b, axis=1):
        return np.linalg.norm(a-b, axis=axis)

    def to_dict(self):
        _dict = {'k': self.k}
        try:
            _dict['n X'] = len(self.X)
            _dict['n centroids'] = len(self.centroids)
        except:
            logging.warning('X has not been set.')
        return _dict

    def fit(self, x, y):
        self.X = list(zip(x, y))
        self.centroids = self.get_centroids()
        logging.info('initial centroids: %s' % self.centroids)
        self.old_centroids = np.zeros(self.centroids.shape)
        self.clusters = np.zeros(len(self.X))
        self.delta = self.get_dist(self.centroids, self.old_centroids, None)

    def get_k(self):
        """TODO: use elbow method to determine k"""
        pass

    def get_centroids(self):
        """get centroids using instance data"""
        c_x = np.random.randint(np.min(self.X), np.max(self.X), size=self.k)
        c_y = np.random.randint(np.min(self.X), np.max(self.X), size=self.k)
        return np.array(list(zip(c_x, c_y)), dtype=np.float32)

    def predict(self, x=None, y=None):
        if x is None or y is None:
            X = self.X
        else:
            X = list(zip(x, y))

        run = 0
        while self.delta != 0:
            for i in range(len(X)):
                distances = self.get_dist(X[i], self.centroids)
                cluster = np.argmin(distances)
                self.clusters[i] = cluster
            self.old_centroids = deepcopy(self.centroids)
            for i in range(self.k):
                points = \
                    [X[j] for j in range(len(X)) if self.clusters[j] == i]
                self.centroids[i] = np.mean(points, axis=0)
            self.delta = \
                self.get_dist(self.centroids, self.old_centroids, None)
            logging.info('run: %s new delta: %s' % (run, self.delta))
            if np.isnan(self.delta):
                logging.error('failed to utilize k-centroids') # TODO: debug
                break
            run += 1

class DBSCAN:
    def __init__(self):
        pass
