import unittest
import matplotlib.pyplot as plt
from dasy.synthesizers.uniform import UniformSynth
from dasy.labelers.regression.linear import LinearRegressionLabeler

class TestRegressionLabelers(unittest.TestCase):
    def test_linear_labeler(self):
        dim = 1
        n = 50
        synth = UniformSynth()
        labeler = LinearRegressionLabeler(dim=dim)
        X = synth.sample(n=n, dim=dim)
        y = labeler.assign(X)
        #print(X.shape)
        #print(y.shape)

        plt.clf()
        plt.scatter(X.T[0], y)
        plt.axline((0, labeler.b), slope=labeler.w, color='r')
        plt.title('Uniform Data x with Linear y + noise')
        plt.tight_layout()
        plt.savefig('linear_labeler')

