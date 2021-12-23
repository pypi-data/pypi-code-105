import os, sys
import numpy as np
import py3toolbox as tb
import tensorflow_datasets as tfds

import matplotlib.pyplot as plt

from sklearn.preprocessing import normalize
from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs, make_moons
from sklearn.datasets import make_gaussian_quantiles

def parse_dataset(dataset):
  data    = dataset[:,:-1]
  labels  = np.squeeze(np.asarray(dataset[:,-1:].T))  # last column is labels
  return data, labels


def print_dataset_info (train_data, train_labels, test_data, test_labels, output_folder=None ):
  output =  ("Train Data    Shape  (numpy) : " + str(train_data.shape))   + "\n" 
  output += ("Train Labels  Shape  (numpy) : " + str(train_labels.shape)) + "\n"
  output += ("Test  Data    Shape  (numpy) : " + str(test_data.shape))    + "\n"
  output += ("Test  Labels  Shape  (numpy) : " + str(test_labels.shape)) 
  if output_folder is not None:
    data_set_meta_file = output_folder + "/dataset.info.txt"
    tb.write_file(file_name=data_set_meta_file, text=output, mode = "w")
    print (output)
    


########################################################################
#
# 2D Toy dataset
#
########################################################################

def gen_2d_toy_dataset(n_samples=5000, centers=5, random_seed = None, train_test_ratio=0.8, cluster_std=1.0, show=False, type="blob"):

  # generate sample data
  if type=="blob" :
    X1, Y1 = make_blobs(n_samples=n_samples, centers=centers, n_features=2, random_state=random_seed, cluster_std=cluster_std)
  
  if type == "moon" :
    X1, Y1 = make_moons(n_samples=n_samples, noise=cluster_std, random_state=random_seed)


  # normalize data
  X1 = normalize(X1, axis=0, norm='max')
  
  # show plot if required
  if show : 
    plt.figure(figsize=(1, 1))
    plt.scatter(X1[:, 0], X1[:, 1], marker="o", c=Y1, s=25, edgecolor="k")
    plt.show()
    
  # show plot if required
  X1 = np.asmatrix(X1)
  Y1 = np.asmatrix(Y1)

  sample_dataset = np.concatenate((X1, Y1.T), axis=1)
  np.random.shuffle(sample_dataset) 

  # split into train and test
  train_dataset = sample_dataset[:int(n_samples*train_test_ratio)]
  test_dataset  = sample_dataset[int(n_samples*train_test_ratio):]

  train_data, train_labels    = parse_dataset (train_dataset)
  test_data , test_labels     = parse_dataset(test_dataset)
     
  # output data shapes
  print_dataset_info (train_data,train_labels, test_data, test_labels )
  return ((train_data, train_labels), (test_data, test_labels))


########################################################################
#
# TF dataset
#
########################################################################
def load_tf_dataset(dataset_name="mnist"):
  """
    Load Tensorflow Datasets
    Save the result datasets into Train and Test
  
  """
  ds_train, ds_test = tfds.load(name=dataset_name,
                       split = ['train', 'test'], 
                       batch_size = -1,
                       as_supervised=True)


  # to shuffle
  #ds_train = ds_train.shuffle(buffer_size=10)  
  #ds_test  = ds_test.shuffle(buffer_size=10)  


  (train_data, train_labels)        =   tfds.as_numpy(ds_train)
  (test_data, test_labels)          =   tfds.as_numpy(ds_test)

  print_dataset_info (train_data,train_labels, test_data, test_labels )
  return ((train_data, train_labels), (test_data, test_labels))
  
  
if __name__ == '__main__':
  ((train_data, train_labels), (test_data, test_labels)) = gen_2d_toy_dataset(n_samples=1000, cluster_std=0.2, type="moon", show=True)
  print (train_data)
  print (train_labels)
  print (train_data[:,0].max(axis=0))
