import numpy as np
import pandas as pd
import torch
from torch.autograd import Variable

from sklearn.preprocessing import MinMaxScaler

def sliding_windows(data, seq_length):
    x = []
    y = []

    for i in range(len(data)-seq_length-1):
        _x = data[i:(i+seq_length)]
        _y = data[i+seq_length]
        x.append(_x)
        y.append(_y)

    return np.array(x),np.array(y)


class LoadCsv():
	def __init__(self,filepath = r'airline-passengers.csv'):  #r'airline-passengers.csv' is it a default data??
		self.df = pd.read_csv(filepath)
		#training_set = pd.read_csv('shampoo.csv')
		self.y = self.df.iloc[:,1:2].values

## todo make class abstractions::::

class DataLoader():
	def __init__(self,filepath,fraction=0.67):
		self.df = pd.read_csv(filepath)
		#training_set = pd.read_csv('shampoo.csv')
		self.y = self.df.iloc[:,1:2].values

		self.sc = MinMaxScaler()
		training_data = self.sc.fit_transform(self.y)

		self.seq_length = 4
		x, y = sliding_windows(training_data, self.seq_length)

		train_size = int(len(y) * fraction)
		self.train_size = train_size
		self.test_size = len(y) - train_size

		self.X = Variable(torch.Tensor(np.array(x)))
		self.Y = Variable(torch.Tensor(np.array(y)))

		self.trainX = Variable(torch.Tensor(np.array(x[0:train_size])))
		self.trainY = Variable(torch.Tensor(np.array(y[0:train_size])))

		self.testX = Variable(torch.Tensor(np.array(x[train_size:len(x)])))
		self.testY = Variable(torch.Tensor(np.array(y[train_size:len(y)])))


#class DataLoader():
#	def __init__(self,path):
