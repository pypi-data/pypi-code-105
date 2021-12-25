import numpy as np
import pandas as pd

def fit(x,y):
    matrix_a = []
    for i in range(len(x.columns)+1):
        line = []
        if i == 0:
            for j in range(len(x.columns)+1):
                if j == 0:
                    line.append(len(x))
                else:
                    line.append(sum(x.iloc[:,j-1]))
        else:
            for j in range(len(x.columns)+1):
                if j == 0:
                    line.append(sum(x.iloc[:,i-1]))
                elif j == i:
                    square = sum(x.iloc[:,i-1]**2)
                    line.append(square)
                else:
                    multiply = sum(x.iloc[:,i-1]*x.iloc[:,j-1])
                    line.append(multiply)
        matrix_a.append(line)
        
    matrix_h = []
    for i in range(len(x.columns)+1):
        if i == 0:
            matrix_h.append(sum(y))
        else:
            matrix_h.append(sum(y*x.iloc[:,i-1]))
            
    matrix = []
    for i in range(len(x.columns)+1):
        array = np.array(matrix_a)
        array[:,i] = matrix_h
        matrix.append(array)
        
    matrix_det = []
    for i in range(len(x.columns)+2):
        if i == 0:
            array = np.array(matrix_a)
            det_a = np.linalg.det(array)
            matrix_det.append(det_a)
        else:
            array = matrix[i-1]
            det_a = np.linalg.det(array)
            matrix_det.append(det_a)
            
    coefficient = []
    for i in range(len(matrix_det)):
        if i == 0:
            continue
        else:
            result = matrix_det[i]/matrix_det[0]
            coefficient.append(result)
            
    a = coefficient[0]
    b = []
    for i in range(1,len(coefficient)):
        b.append(coefficient[i])    
    return a,b

def predict(x,y,test):
    prediction = []
    for i in range(len(test)):
        slope_var = []
        for j in range(len(test.columns)):
            multiply = test.iloc[i][j]*fit(x,y)[1][j]
            slope_var.append(multiply)
        result = fit(x,y)[0] + sum(slope_var)
        prediction.append(result)    
    return prediction
        
def intercept(x,y):
    return fit(x,y)[0]

def slope(x,y):
    return fit(x,y)[1]

def rsquare(x,y):
    y_hat = []
    for i in range(len(x)):
        slope_var = []
        for j in range(len(x.columns)):
            multiply = x.iloc[i][j]*fit(x,y)[1][j]
            slope_var.append(multiply)
        result = fit(x,y)[0] + sum(slope_var)
        y_hat.append(result)
        
    sst,sse = [],[]
    for i in range(len(y)):
        mean_min = (y.tolist()[i]-sum(y)/len(y))**2
        sst.append(mean_min)
    for i in range(len(y)):
        hat_min = (y.tolist()[i]-y_hat[i])**2
        sse.append(hat_min)
    r_square = 1-(sum(sse)/sum(sst))
    return r_square

def r(x,y):
    multiple_r = rsquare(x,y)**(1/2)
    return multiple_r

def info(x,y):
    print('Constant : ',fit(x,y)[0])
    for i in range(len(fit(x,y)[1])):
        print(f'Coefficient_{i+1} : {fit(x,y)[1][i]}')
    print('Multiple R : ',r(x,y))
    print('R Squared : ',rsquare(x,y))