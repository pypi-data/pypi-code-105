# --- built in ---
import os
import sys
import time
import math

# --- 3rd party ---
import numpy as np

# --- my module ---

__all__ = [
    'sample_2d'
]

# Borrowed from this repo
#    https://github.com/kamenbliznashki/normalizing_flows

def sample_2d(dataset, n_samples):

    z = np.random.normal(size=(n_samples, 2))

    if dataset == '8gaussians':
        scale = 4
        sq2 = 1/math.sqrt(2)
        centers = [(1,0), (-1,0), (0,1), (0,-1), (sq2,sq2), (-sq2,sq2), (sq2,-sq2), (-sq2,-sq2)]
        centers = np.asarray([(scale * x, scale * y) for x,y in centers])
        return sq2 * (0.5 * z + centers[np.random.randint(len(centers), size=(n_samples,))])

    elif dataset == '2spirals':
        n = np.sqrt(np.random.rand(n_samples // 2)) * 540 * (2 * math.pi) / 360
        d1x = - np.cos(n) * n + np.random.rand(n_samples // 2) * 0.5
        d1y =   np.sin(n) * n + np.random.rand(n_samples // 2) * 0.5
        x = np.concatenate([np.stack([ d1x,  d1y], axis=1),
                            np.stack([-d1x, -d1y], axis=1)], axis=0) / 3
        return x + 0.1*z

    elif dataset == 'checkerboard':
        x1 = np.random.rand(n_samples) * 4 - 2
        x2_ = np.random.rand(n_samples) - np.random.randint(0, 2, (n_samples,)).astype(np.float32) * 2
        x2 = x2_ + np.floor(x1) % 2
        return np.stack([x1, x2], axis=1) * 2

    elif dataset == 'rings':
        n_samples4 = n_samples3 = n_samples2 = n_samples // 4
        n_samples1 = n_samples - n_samples4 - n_samples3 - n_samples2

        # so as not to have the first point = last point, set endpoint=False in np; here shifted by one
        linspace4 = np.linspace(0, 2 * math.pi, n_samples4 + 1)[:-1]
        linspace3 = np.linspace(0, 2 * math.pi, n_samples3 + 1)[:-1]
        linspace2 = np.linspace(0, 2 * math.pi, n_samples2 + 1)[:-1]
        linspace1 = np.linspace(0, 2 * math.pi, n_samples1 + 1)[:-1]

        circ4_x = np.cos(linspace4)
        circ4_y = np.sin(linspace4)
        circ3_x = np.cos(linspace4) * 0.75
        circ3_y = np.sin(linspace3) * 0.75
        circ2_x = np.cos(linspace2) * 0.5
        circ2_y = np.sin(linspace2) * 0.5
        circ1_x = np.cos(linspace1) * 0.25
        circ1_y = np.sin(linspace1) * 0.25

        x = np.stack([np.concatenate([circ4_x, circ3_x, circ2_x, circ1_x]),
                      np.concatenate([circ4_y, circ3_y, circ2_y, circ1_y])], axis=1) * 3.0

        # random sample
        x = x[np.random.randint(0, n_samples, size=(n_samples,))]

        # Add noise
        return x + np.random.normal(scale=0.08, size=x.shape)

    else:
        raise RuntimeError('Invalid `dataset` to sample from.')
