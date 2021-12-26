
# random search logistic regression model on the sonar dataset
from scipy.stats import loguniform
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import RandomizedSearchCV
import os
import math
from sklearn.utils.multiclass import type_of_target
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.model_selection import cross_val_score

# load dataset
dataframe = pd.read_csv(str(os.getcwd() + '/data_library/6_Emerging_Markets_8years.csv'), header=None)
# split into input and output elements
data = dataframe.values
X, y = data[:, -2:-1], data[:, -1]

type_of_target(y)
y = LabelEncoder().fit_transform(y)




class RegularizedRegressor:
    def __init__(self, l = 0.01):
        self.l = l

    def combine(self, inputs):
        return sum([i*w for (i,w) in zip([1] + inputs, self.weights)])

    def predict(self, X):
        return [self.combine(x) for x in X]

    def fit(self, X, y, **kwargs):
        for value_l in kwargs['l']:
            self.l = value_l
            (numElementsx, N) = X.shape
            (numElementsy) = y.shape*kwargs['l']
            W = (X.transpose() * X) * X.transpose() * y
            self.weights = [w[0] for w in W.tolist()]
            return self

    def get_params(self, deep = False):
        return {'l':self.l}




result = cross_val_score(RegularizedRegressor(),X,y, fit_params={'l':[0.1]},scoring = 'accuracy')

print('SUCCESS')

#print('Best Score: %s' % result.best_score_)
#print('Best Hyperparameters: %s' % result.best_params_)










