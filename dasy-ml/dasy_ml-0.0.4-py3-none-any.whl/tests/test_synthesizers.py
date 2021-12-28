import unittest
import numpy as np
import matplotlib.pyplot as plt
from dasy.synthesizers.uniform import UniformSynth 
from dasy.synthesizers.gaussian import GaussianSynth 

class TestSynthesizers(unittest.TestCase):
    def test_uniform_synth(self):
        plt.clf()
        dim = 2
        n = 50

        synth = UniformSynth()
        low = -.5
        high = .5 
        data = synth.sample(n=n, dim=dim, low=low, high=high)
        # test boundaries
        for x in data:
            self.assertTrue(np.all(x < high))
            self.assertTrue(np.all(x > low))

        plt.scatter(data.T[0], data.T[1])
        plt.title('Uniform Data')
        plt.tight_layout()
        plt.savefig('uniform_data')

    def test_gaussian_synth(self):
        plt.clf()
        dim = 2
        n = 100

        synth = GaussianSynth()
        data = synth.sample(n=n, dim=dim)

        plt.scatter(data.T[0], data.T[1])
        plt.title('Gaussian Data')
        plt.tight_layout()
        plt.savefig('gaussian_data')

