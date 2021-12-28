import numpy as np
from dasy.core import Labeler

class CentroidsLabeler(Labeler):
    """
    Creates a centroid for each class and labels points according to 
    which is the closest centroid (similar to the first step of k-means).
    This is a deterministic labeler. 
    """
    def __init__(self, classes=2, dim=2):
        super().__init__(classes=classes)
        self.dim = dim
        self.centroids = np.random.normal(size=(classes, dim))

    def assign(self, X):
        y = np.zeros(len(X))
        for i in range(len(X)):
            y[i] = self.nearest_centroid(X[i], self.centroids)
        return y

    def nearest_centroid(self, x, centroids):
        dists = np.linalg.norm(x - centroids, axis=1)
        return np.argmin(dists)




        
