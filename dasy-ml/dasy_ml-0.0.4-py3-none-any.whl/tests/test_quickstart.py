import unittest
import numpy as np
import matplotlib.pyplot as plt
from dasy.synthesizers.gaussian import GaussianSynth
from dasy.synthesizers.uniform import UniformSynth
from dasy.labelers.classification.centroids import CentroidsLabeler
from dasy.labelers.regression.linear import LinearRegressionLabeler

class TestQuickstart(unittest.TestCase):
    def test_quickstart(self):
        plt.clf()
### dasy for classification
# 1. Define the problem
        dim = 2 # dimension of each input
        classes = 2 # number of classes
        n = 100 # number of data points
# 2. Create synthetic input data X
        synth = GaussianSynth() 
        X = synth.sample(n=n, dim=dim) # sample n dim-dimensional data points from Gaussian
# 3. Assign labels y
        labeler = CentroidsLabeler(classes=classes, dim=dim) # for 2 classes, this creates linearly separable labels
        y = labeler.assign(X)
# 4. Plot
        plt.scatter(X.T[0], X.T[1], c=y)
        plt.title('Synthetic Classification Problem')
        plt.tight_layout()
        plt.savefig('synthetic_classification')
        plt.clf()

### dasy for regression
# 1. Define the problem
        dim = 1 # dimension of each input
        n = 50 # number of data points
# 2. Create synthetic input data X
        synth = UniformSynth() 
        X = synth.sample(n=n, dim=dim) # sample n dim-dimensional data points from Uniform distribution
# 3. Assign continuous targets y
        labeler = LinearRegressionLabeler(dim=dim)
        y = labeler.assign(X)
# 4. Plot
        plt.scatter(X.T[0], y)
        plt.axline((0, labeler.b), slope=labeler.w, color='r') # plot the underlying line which generated the targets
        plt.title('Synthetic Regression Problem')
        plt.tight_layout()
        plt.savefig('synthetic_regression')
