from copy import deepcopy
import random
import numpy as np
import logging


class KMeans:
    def __init__(self, k=8, viz=None):
        self.k = k
        self.viz = viz

    @staticmethod
    def get_dist(a, b, axis=1):
        return np.linalg.norm(a-b, axis=axis)

    def to_dict(self):
        _dict = {'k': self.k}
        try:
            _dict['n X'] = len(self.X)
            nonnull = ~np.isnan(self.centroids)
            _dict['n centroids'] = len(self.centroids[nonnull.all(axis=1)])
        except:
            logging.warning('X has not been set.')
        return _dict

    def fit(self, x, y):
        self.x = x
        self.y = y
        self.X = list(zip(x, y))
        self.centroids = self.get_centroids()
        if self.viz:
            self.viz.x1 = x
            self.viz.y1 = y
            x2 = [c[0] for c in self.centroids]
            y2 = [c[1] for c in self.centroids]
            self.viz.update(x2, y2)
        logging.info('initial centroids: %s' % self.centroids)
        self.old_centroids = np.zeros(self.centroids.shape)
        self.clusters = np.zeros(len(self.X), dtype=np.int32)
        self.delta = self.get_dist(self.centroids, self.old_centroids, None)

    def get_k(self):
        """TODO: use elbow method to determine k"""
        pass

    def get_centroids(self):
        """get centroids using instance data"""
        c_x = np.random.randint(np.min(self.x), np.max(self.x), size=self.k)
        c_y = np.random.randint(np.min(self.y), np.max(self.y), size=self.k)
        return np.array(list(zip(c_x, c_y)), dtype=np.float32)

    def predict(self, x=None, y=None):
        if x is None or y is None:
            X = list(self.X)
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
            if self.viz:
                x2 = [c[0] for c in self.centroids]
                y2 = [c[1] for c in self.centroids]
                self.viz.update(x2, y2)
            run += 1

class DBSCAN:
    def __init__(self, x, y, epsilon=0.5, minpts=2, viz=None):
        self.epsilon = epsilon
        self.minpts = minpts
        self.viz = viz

    def to_dict(self):
        _dict = {'epsilon': self.epsilon, 'minpts': self.minpts}
        try:
            _dict['n X'] = len(self.X)
        except:
            logging.warning('X has not been set.')
        return _dict

    def fit(self, x, y):
        self.X = list(zip(x, y))
        self.clusters = np.zeros(len(self.X), dtype=np.int32)
        if self.viz:
            self.viz.x = x
            self.viz.y = y
            self.viz.update(self.clusters)

    @staticmethod
    def get_neighbors(X, i, epsilon):
        neighbors = []
        for j in range(0, len(X)):
            a = np.array(X[i])
            b = np.array(X[j])
            if np.linalg.norm(a-b) < epsilon:
                neighbors.append(j)
        return neighbors

    def build_cluster(self, i, neighbors, cluster):
        self.clusters[i] = cluster
        for j in neighbors:
            if self.clusters[j] == -1:
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
                self.clusters[i] = -1
            else:
                cluster += 1
                self.build_cluster(i, points, cluster)
            if self.viz:
                self.viz.update(self.clusters)
