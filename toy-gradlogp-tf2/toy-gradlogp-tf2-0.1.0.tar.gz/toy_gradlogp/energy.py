# --- built in ---
import os
import sys
import time
import math
import logging
import functools

# --- 3rd party ---
import numpy as np
import tensorflow as tf

# --- my module ---

__all__ = [
    'ToyMLP',
    'Energy',
    'Trainer',
]

# --- primitives ---

class ToyMLP(tf.keras.Model):
    def __init__(
        self,
        input_dim=2,
        output_dim=1,
        units=[300, 300],
        silu=True,
        dropout=False
    ):
        """Toy MLP from
        https://github.com/ermongroup/ncsn/blob/master/runners/toy_runner.py#L198
        Args:
            input_dim (int, optional): input dimensions. Defaults to 2.
            output_dim (int, optional): output dimensions. Defaults to 1.
            units (list, optional): hidden units. Defaults to [300, 300].
            silu (bool, optional): use silu as activation function. Set False to use
                soft plus instead. Defaults to True.
            dropout (bool, optional): use dropout layers. Defaults to False.
        """
        super().__init__()
        layers = [tf.keras.layers.Flatten()]
        for unit in units:
            layers.extend([
                tf.keras.layers.Dense(unit),
                tf.keras.layers.Activation('silu' if silu else 'softplus'),
                tf.keras.layers.Dropout(.5) if dropout else tf.keras.layers.Layer()
            ])
        layers.append(tf.keras.layers.Dense(output_dim))

        self.net = tf.keras.Sequential(layers)
        # forwrad dummy tensor
        dummy = tf.keras.Input((input_dim,), dtype=tf.float32)
        self.net(dummy)

    def call(self, x, training=True):
        return self.net(x, training=training)

# --- energy model ---
class Energy(tf.keras.Model):
    def __init__(self, net):
        """A simple energy model

        Args:
            net (tf.keras.Model): An energy function, the output shape of
                the energy function should be (b, 1). The score is
                computed by grad(-E(x))
        """
        super().__init__()
        self.net = net

    def call(self, x, training=True):
        return self.net(x, training=training)

    def score(self, x, sigma=None, training=True):
        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(x)
            logp = -tf.math.reduce_sum(self.net(x, training=training))
        grad = tape.gradient(logp, x)
        return grad

class Trainer():
    def __init__(
        self,
        model,
        learning_rate = 1e-3,
        clipnorm = 100.,
        n_slices = 1,
        loss_type = 'ssm-vr',
        noise_type = 'gaussian',
    ):
        """Energy based model trainer

        Args:
            model (nn.Module): energy-based model
            learning_rate (float, optional): learning rate. Defaults to 1e-4.
            clipnorm (float, optional): gradient clip. Defaults to 100..
            n_slices (int, optional): number of slices for sliced score matching loss.
                Defaults to 1.
            loss_type (str, optional): type of loss. Can be 'ssm-vr', 'ssm', 'deen',
                'dsm'. Defaults to 'ssm-vr'.
            noise_type (str, optional): type of noise. Can be 'radermacher', 'sphere'
                or 'gaussian'. Defaults to 'radermacher'.
        """
        self.model = model
        self.learning_rate = learning_rate
        self.clipnorm = clipnorm
        self.n_slices = n_slices
        self.loss_type = loss_type.lower()
        self.noise_type = noise_type.lower()
        # setup optimizer
        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=learning_rate,
            clipnorm=clipnorm
        )
        
        self.num_gradsteps = 0
        self.num_epochs = 0
        self.progress = 0
        self.tb_writer = None

    def ssm_loss(self, x, v):
        """SSM loss from
        Sliced Score Matching: A Scalable Approach to Density and Score Estimation

        The loss is computed as
        s = -dE(x)/dx
        loss = vT*(ds/dx)*v + 1/2*(vT*s)^2

        Args:
            x (tf.Tensor): input samples
            v (tf.Tensor): sampled noises

        Returns:
            SSM loss
        """
        x = tf.repeat(x, self.n_slices, axis=0) # (n_slices*b, ...)
        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(x)
            score = self.model.score(x) # (n_slices*b, ...)
            sv    = tf.math.reduce_sum(score * v) # ()
        gsv = tape.gradient(sv, x) # (n_slices*b, ...)
        loss1 = tf.math.reduce_sum(score * v, axis=-1) ** 2 * 0.5 # (n_slices*b,)
        loss2 = tf.math.reduce_sum(v * gsv, axis=-1) # (n_slices*b,)
        loss = tf.math.reduce_mean(loss1 + loss2) # ()
        return loss
    
    def ssm_vr_loss(self, x, v):
        """SSM-VR (variance reduction) loss from
        Sliced Score Matching: A Scalable Approach to Density and Score Estimation

        The loss is computed as
        s = -dE(x)/dx
        loss = vT*(ds/dx)*v + 1/2*||s||^2

        Args:
            x (tf.Tensor): input samples
            v (tf.Tensor): sampled noises

        Returns:
            SSM-VR loss
        """
        x = tf.repeat(x, self.n_slices, axis=0) # (n_slices*b, ...)
        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(x)
            score = self.model.score(x) # (n_slices*b, ...)
            sv    = tf.math.reduce_sum(score * v) # ()
        gsv = tape.gradient(sv, x) # (n_slices*b, ...)
        loss1 = tf.norm(score, axis=-1) ** 2 * 0.5 # (n_slices*b,)
        loss2 = tf.math.reduce_sum(v*gsv, axis=-1) # (n_slices*b,)
        loss = tf.math.reduce_mean(loss1 + loss2) # ()
        return loss
    
    def deen_loss(self, x, v, sigma=0.1):
        """DEEN loss from
        Deep Energy Estimator Networks

        The loss is computed as
        x_ = x + v   # noisy samples
        s = -dE(x_)/dx_
        loss = 1/2*||x - x_ + sigma^2*s||^2

        Args:
            x (tf.Tensor): input samples
            v (tf.Tensor): sampled noises
            sigma (int, optional): noise scale. Defaults to 1.

        Returns:
            DEEN loss
        """
        v = v * sigma
        x_ = x + v
        s = (sigma ** 2) * self.model.score(x_)
        loss = tf.norm(s+v, axis=-1)**2
        loss = 0.5 * tf.math.reduce_mean(loss)
        return loss

    def dsm_loss(self, x, v, sigma=0.1):
        """DSM loss from
        A Connection Between Score Matching
            and Denoising Autoencoders

        The loss is computed as
        x_ = x + v   # noisy samples
        s = -dE(x_)/dx_
        loss = 1/2*||s + (x-x_)/sigma^2||^2

        Args:
            x (tf.Tensor): input samples
            v (tf.Tensor): sampled noises
            sigma (float, optional): noise scale. Defaults to 0.1.
        
        Returns:
            DSM loss
        """
        v = v * sigma
        x_ = x + v
        s = self.model.score(x_)
        loss = tf.norm(s + v/(sigma**2), axis=-1) ** 2
        loss = 0.5 * tf.math.reduce_mean(loss)
        return loss

    def get_random_noise(self, x, n_slices=None):
        """Sampling random noises

        Args:
            x (tf.Tensor): input samples
            n_slices (int, optional): number of slices. Defaults to None.

        Returns:
            tf.Tensor: sampled noises
        """
        if n_slices is None:
            v = tf.random.normal(x.shape)
        else:
            v = tf.random.normal((n_slices, *x.shape))
            v = tf.reshape(v, (-1, *v.shape[2:])) # (n_slices*b, 2)

        if self.noise_type == 'radermacher':
            v = tf.math.sign(v)
        elif self.noise_type == 'sphere':
            v = v/tf.norm(v, axis=-1, keepdims=True) * np.sqrt(v.shape[-1])
        elif self.noise_type == 'gaussian':
            pass
        else:
            raise NotImplementedError(
                f"Noise type '{self.noise_type}' not implemented."
            )
        return v
            
    
    def get_loss(self, x, v=None):
        """Compute loss

        Args:
            x (tf.Tensor): input samples
            v (tf.Tensor, optional): sampled noises. Defaults to None.

        Returns:
            loss
        """
        if self.loss_type == 'ssm-vr':
            v = self.get_random_noise(x, self.n_slices)
            loss = self.ssm_vr_loss(x, v)
        elif self.loss_type == 'ssm':
            v = self.get_random_noise(x, self.n_slices)
            loss = self.ssm_loss(x, v)
        elif self.loss_type == 'deen':
            v = self.get_random_noise(x, None)
            loss = self.deen_loss(x, v)
        elif self.loss_type == 'dsm':
            v = self.get_random_noise(x, None)
            loss = self.dsm_loss(x, v)
        else:
            raise NotImplementedError(
                f"Loss type '{self.loss_type}' not implemented."
            )

        return loss
    
    @tf.function
    def train_step(self, batch, update=True):
        """Train one batch

        Args:
            batch (dict): batch data
            update (bool, optional): whether to update networks. 
                Defaults to True.

        Returns:
            loss
        """
        x = batch['samples']
        # move inputs to device
        x = tf.convert_to_tensor(x, dtype=tf.float32)
        vars = self.model.variables
        with tf.GradientTape() as tape:
            tape.watch(vars)
            # compute losses
            loss = self.get_loss(x)
        # update model
        if update:
            # compute gradients
            grads = tape.gradient(loss, vars)
            self.optimizer.apply_gradients(zip(grads, vars))
        return loss

    def train(self, dataset, batch_size):
        """Train one epoch

        Args:
            dataset (tf.data.Dataset): Tensorflow dataset
            batch_size (int): batch size

        Returns:
            np.ndarray: mean loss
        """        
        all_losses = []
        dataset = dataset.batch(batch_size)
        for batch_data in dataset.as_numpy_iterator():
            sample_batch = {
                'samples': batch_data
            }
            loss = self.train_step(sample_batch)
            self.num_gradsteps += 1
            all_losses.append(loss)
        m_loss = np.mean(all_losses).astype(np.float32)
        return m_loss

    def eval(self, dataset, batch_size):
        """Eval one epoch

        Args:
            dataset (tf.data.Dataset): Tensorflow dataset
            batch_size (int): batch size

        Returns:
            np.ndarray: mean loss
        """        
        all_losses = []
        dataset = dataset.batch(batch_size)
        for batch_data in dataset.as_numpy_iterator():
            sample_batch = {
                'samples': batch_data
            }
            loss = self.train_step(sample_batch, update=False)
            all_losses.append(loss)
        m_loss = np.mean(all_losses).astype(np.float32)
        return m_loss

    def learn(
        self,
        train_dataset,
        eval_dataset = None,
        n_epochs = 5,
        batch_size = 100,
        log_freq = 1,
        eval_freq = 1,
        vis_freq = 1,
        vis_callback = None,
        tb_logdir = None
    ):
        """Train the model

        Args:
            train_dataset (tf.data.Dataset): training dataset
            eval_dataset (tf.data.Dataset, optional): evaluation dataset.
                Defaults to None.
            n_epochs (int, optional): number of epochs to train. Defaults to 5.
            batch_size (int, optional): batch size. Defaults to 100.
            log_freq (int, optional): logging frequency (epoch). Defaults to 1.
            eval_freq (int, optional): evaluation frequency (epoch). Defaults to 1.
            vis_freq (int, optional): visualizing frequency (epoch). Defaults to 1.
            vis_callback (callable, optional): visualization function. Defaults to None.
            tb_logdir (str, optional): path to tensorboard files. Defaults to None.

        Returns:
            self
        """        
        if tb_logdir is not None:
            self.tb_writer = tf.summary.create_file_writer(tb_logdir)

        # initialize
        time_start = time.time()
        time_spent = 0
        total_epochs = n_epochs

        for epoch in range(n_epochs):
            self.num_epochs += 1
            self.progress = float(self.num_epochs) / float(n_epochs)
            # train one epoch
            loss = self.train(train_dataset, batch_size)
            # write tensorboard
            if self.tb_writer is not None:
                with self.tb_writer.as_default():
                    tf.summary.scalar(f'train/loss', loss, step=self.num_epochs)
            
            if (log_freq is not None) and (self.num_epochs % log_freq == 0):
                logging.info(
                    f"[Epoch {self.num_epochs}/{total_epochs}]: loss: {loss}"
                )

            if (eval_dataset is not None) and (self.num_epochs % eval_freq == 0):
                # evaluate
                eval_loss = self.eval(eval_dataset, batch_size)

                if self.tb_writer is not None:
                    with self.tb_writer.as_default():
                        tf.summary.scalar(f'eval/loss', eval_loss, step=self.num_epochs)
                
                logging.info(
                    f"[Eval {self.num_epochs}/{total_epochs}]: loss: {eval_loss}"
                )

            if (vis_callback is not None) and (self.num_epochs % vis_freq == 0):
                logging.debug("Visualizing")
                vis_callback(self)
        return self
