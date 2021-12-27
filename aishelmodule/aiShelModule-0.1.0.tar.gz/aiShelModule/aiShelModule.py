import numpy as np

def count(arr):
	return np.bincount(arr)

def get_unique(arr):
	return np.unique(arr)