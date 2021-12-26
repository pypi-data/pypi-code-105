from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import pandas as pd

data = np.matrix(pd.read_csv('/Users/franciscoantonioprietorodriguez/Documents/Git_repositories/pystrategy/pystrategy/default_data/6_Emerging_Markets_8years.csv', header=None))



k_range = range(1, 30)
print(k_range)

param_grid = dict(n_neighbors = k_range)
print (param_grid)


knn = KNeighborsClassifier(n_neighbors=5)
grid = GridSearchCV(knn, param_grid, cv = 10, scoring='accuracy')


def rolling_windows_validation(wubc):
    # Save number of elements and number of assets
    (numData, N) = wubc.dataValidation.shape

    # Initialize the weights matrix
    W = np.zeros((wubc().validation_windows, N))

    for i in range(0, wubc().validation_windows):
        W[[i]] = np.transpose(wubc.solve_optimization_problem(
            wubc.dataValidation[i:numData - (wubc().validation_windows + (i)), :], wubc().validation_windows))

    a = W
    b = (wubc.dataValidation[wubc.dataValidation.shape[0] - wubc().validation_windows:, :])
    return np.multiply(a, b).sum(axis=1, dtype='float')


def error_loss(lamb, upper_bound):
    wubc.lamb = lamb
    wubc.upper_bound = upper_bound
    returns = rolling_windows_validation(wubc)
    value = np.std(returns) / returns.


(variable, N) = data.shape
# Create the validation set
dataValidation = data[0:-32:, :]