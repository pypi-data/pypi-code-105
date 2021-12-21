# --- built in ---
import os

# --- 3rd party ---
import numpy as np

# --- my module ---
import tensorflow as tf

__all__ = [
    'langevin_dynamics',
    'anneal_langevin_dynamics',
    'sample_score_field',
    'sample_energy_field'
]


# --- dynamics ---
def langevin_dynamics(
    score_fn,
    x,
    eps=0.1,
    n_steps=1000
):
    """Langevin dynamics

    Args:
        score_fn (callable): a score function with the following sign
            func(x: tf.Tensor) -> tf.Tensor
        x (tf.Tensor): input samples
        eps (float, optional): noise scale. Defaults to 0.1.
        n_steps (int, optional): number of steps. Defaults to 1000.
    """
    for i in range(n_steps):
        x = x + eps/2. * np.asarray(score_fn(x))
        x = x + np.random.normal(size=x.shape) * np.sqrt(eps)
    return x

def anneal_langevin_dynamics(
    score_fn,
    x,
    sigmas=None,
    eps=0.1,
    n_steps_each=100
):
    """Annealed Langevin dynamics

    Args:
        score_fn (callable): a score function with the following sign
            func(x: tf.Tensor, sigma: float) -> tf.Tensor
        x (tf.Tensor): input samples
        sigmas (tf.Tensor, optional): noise schedule. Defualts to None.
        eps (float, optional): noise scale. Defaults to 0.1.
        n_steps (int, optional): number of steps. Defaults to 1000.
    """
    # default sigma schedule
    if sigmas is None:
        sigmas = np.exp(np.linspace(np.log(20), 0., 10))

    for sigma in sigmas:
        for i in range(n_steps_each):
            cur_eps = eps * (sigma / sigmas[-1]) ** 2
            x = x + cur_eps/2. * np.asarray(score_fn(x, sigma))
            x = x + np.random.normal(size=x.shape) * np.sqrt(eps)
    return x


# --- sampling utils ---
def sample_score_field(
    score_fn,
    range_lim=4,
    grid_size=50,
):
    """Sampling score field from an energy model

    Args:
        score_fn (callable): a score function with the following sign
            func(x: tf.Tensor) -> tf.Tensor
        range_lim (int, optional): Range of x, y coordimates. Defaults to 4.
        grid_size (int, optional): Grid size. Defaults to 50.
    """
    mesh = []
    x = np.linspace(-range_lim, range_lim, grid_size)
    y = np.linspace(-range_lim, range_lim, grid_size)
    for i in x:
        for j in y:
            mesh.append(np.asarray([i, j]))
    mesh = np.stack(mesh, axis=0)
    x = tf.convert_to_tensor(mesh, dtype=tf.float32)
    scores = np.asarray(score_fn(x))
    return mesh, scores

def sample_energy_field(
    energy_fn,
    range_lim=4,
    grid_size=1000,
):
    """Sampling energy field from an energy model

    Args:
        energy_fn (callable): an energy function with the following sign
            func(x: tf.Tensor) -> tf.Tensor
        range_lim (int, optional): range of x, y coordinates. Defaults to 4.
        grid_size (int, optional): grid size. Defaults to 1000.
    """
    energy = []
    x = np.linspace(-range_lim, range_lim, grid_size)
    y = np.linspace(-range_lim, range_lim, grid_size)
    for i in y:
        mesh = []
        for j in x:
            mesh.append(np.asarray([j, i]))
        mesh = np.stack(mesh, axis=0)
        inputs = tf.convert_to_tensor(mesh, dtype=tf.float32)
        e = np.asarray(energy_fn(inputs)).reshape(grid_size)
        energy.append(e)
    energy = np.stack(energy, axis=0) # (grid_size, grid_size)
    return energy