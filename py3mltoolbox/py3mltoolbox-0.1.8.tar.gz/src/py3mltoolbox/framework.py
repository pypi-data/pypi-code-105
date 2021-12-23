import os, sys
import numpy as np
import py3toolbox as tb
import tensorflow as tf


def init_tf():
  from tensorflow.python.platform.tf_logging import _THREAD_ID_MASK
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
  
  # Reduce the GPU Menory Usage
  gpus = tf.config.experimental.list_physical_devices('GPU')
  for gpu in gpus: tf.config.experimental.set_memory_growth(gpu, True)


if __name__ == '__main__':
  pass