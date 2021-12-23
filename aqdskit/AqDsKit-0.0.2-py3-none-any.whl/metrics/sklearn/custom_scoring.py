#######
# To be compatible with sklearn
# https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
# scoring takes y_true and y_pred and returns a single score
#######

import numpy as np

# example of custom scoring metric
def max_diff(y_true, y_pred, **kws):
    diff = np.abs(y_true - y_pred).max()
    return np.log1p(diff)
