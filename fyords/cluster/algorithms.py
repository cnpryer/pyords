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
    def __init__(self, x, y, epsilon=0.5, minpts=2):
        self.epsilon = epsilon
        self.minpts = minpts

    def to_dict(self):
        _dict = {'epsilon': self.epsilon, 'minpts': self.minpts}
        try:
            _dict['n X'] = len(self.X)
        except:
            logging.warning('X has not been set.')
        return _dict

    def fit(self, x, y):
        self.X = list(zip(x, y))
        self.clusters = np.zeros(len(self.X))

    @staticmethod
    def get_neighbors(X, i, epsilon):
        neighbors = []
        for j in range(0, len(X)):
            # TODO: tuple - tuple not accepted; understand
            a = np.array(X[i])
            b = np.array(X[j])
            if np.linalg.norm(a-b) < epsilon:
                neighbors.append(j)
        return neighbors

    def build_cluster(self, i, neighbors, cluster):
        self.clusters[i] = cluster
        for j in neighbors:
            if self.clusters[j] == -1: # TODO: is this redundant (see below)
                self.clusters[j] = cluster
            elif self.clusters[j] == 0:
                self.clusters[j] = cluster
                points = self.get_neighbors(self.X, j, self.epsilon)

                if len(points) >= self.minpts:
                    neighbors += points

    def predict(self, x=None, y=None):
        if x is None or y is None:
            X = self.X
        else:
            X = list(zip(x, y))

        cluster = 0
        for i in range(0, len(X)):
            if not self.clusters[i] == 0:
                continue
            points = self.get_neighbors(X, i, self.epsilon)
            if len(points) < self.minpts:
                self.clusters[i] = -1 # noise
            else:
                cluster += 1
