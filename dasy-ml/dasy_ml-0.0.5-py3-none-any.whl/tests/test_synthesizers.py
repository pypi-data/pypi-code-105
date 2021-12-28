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

        low = -.5
        high = .5 
        synth = UniformSynth(dim=dim, low=low, high=high)
        data = synth.sample(n=n)
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

        synth = GaussianSynth(dim=dim)
        data = synth.sample(n=n)

        plt.scatter(data.T[0], data.T[1])
        plt.title('Gaussian Data')
        plt.tight_layout()
        plt.savefig('gaussian_data')

