import unittest
import numpy as np
import matplotlib.pyplot as plt
from dasy.synthesizers.gaussian import GaussianSynth
from dasy.labelers.classification.centroids import CentroidsLabeler
from dasy.plotting_utils import plot_bisectors

class TestClassificationLabelers(unittest.TestCase):
    def test_centroids_labeler(self):
        dim = 2
        plt.clf()
        #plt.gca().set_aspect('equal', adjustable='box')
        #fig, ax = plt.subplots()
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        f.suptitle('Gaussian Data with Centroids Labeling', y=0.84)
        ax1.set_aspect('equal', adjustable='box')
        ax2.set_aspect('equal', adjustable='box')
        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax2.set_xlim(-2, 2)
        ax2.set_ylim(-2, 2)

        synth = GaussianSynth()
        data = synth.sample(n=100, dim=dim)
        #plt.scatter(data.T[0], data.T[1])
        #plt.show()

        labeler = CentroidsLabeler(classes=2, dim=dim)
        labels = labeler.assign(data)
        ax1.scatter(data.T[0], data.T[1], c=labels)
        ax1.scatter(labeler.centroids.T[0], labeler.centroids.T[1], c='r')
        ax1.plot(labeler.centroids.T[0], labeler.centroids.T[1], '--')
        plot_bisectors(labeler.centroids[0], labeler.centroids[1], ax=ax1)
        ax1.title.set_text('classes=2')
        #plt.show()

        labeler = CentroidsLabeler(classes=3, dim=dim)
        labels = labeler.assign(data)
        ax2.scatter(data.T[0], data.T[1], c=labels)
        ax2.scatter(labeler.centroids.T[0], labeler.centroids.T[1], c='r')
        #plt.plot(labeler.centroids.T[0], labeler.centroids.T[1], '--')
        plot_bisectors(labeler.centroids[0], labeler.centroids[1], ax=ax2)
        plot_bisectors(labeler.centroids[0], labeler.centroids[2], ax=ax2)
        plot_bisectors(labeler.centroids[1], labeler.centroids[2], ax=ax2)
        ax2.title.set_text('classes=3')
        plt.tight_layout()
        plt.savefig('centroids_labeler')

