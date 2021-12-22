import numpy as np

def root_mean_squared_error(y_true, y_pred):
    rmse = np.sqrt(np.square(np.subtract(y_true, y_pred)).mean())
    print(rmse)
    
def root_mean_squared_log_error(y_true, y_pred):
    rmsle = np.sqrt(np.square(np.subtract(np.log(y_pred + 1), np.log(y_true + 1))).mean())
    print(rmsle)

def mean_bias_error(y_true, y_pred):
    mbe = np.mean(np.subtract(y_pred, y_true))
    print(mbe)

def relative_squared_error(y_true, y_pred): 
    se1 = np.sum(np.square(np.subtract(y_true, y_pred)))
    se2 = np.sum(np.square(np.subtract(np.average(y_true), y_true)))
    rse = se1/se2
    print(rse)
    
def relative_absolute_error(y_true, y_pred):
    se1 = np.sum(np.subtract(y_true, y_pred))
    se2 = np.sum(np.subtract(np.average(y_true), y_true))
    rae = se1/se2
    print(rae)