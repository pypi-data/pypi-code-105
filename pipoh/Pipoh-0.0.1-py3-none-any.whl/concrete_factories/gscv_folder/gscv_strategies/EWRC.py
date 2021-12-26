from numpy import array, dot
from qpsolvers import solve_qp
import bayes_opt
from bayes_opt import BayesianOptimization
#from Strategy import errorLoss, rollingWindowsValidation

#Funcion para Trasposición conjugada compleja en Python
from numpy import ndarray
class myarray(ndarray):    
    @property
    def H(self):
        return self.conj().T

from Strategy import getWeights, rollingWindowsValidation
import numpy as np
from sklearn.covariance import EmpiricalCovariance
from sklearn.datasets import make_gaussian_quantiles

from scipy.optimize import basinhopping

class EWRC:
    def __init__(self, data):
        self.data = []
    pass
    
    #The Equally Weighted Minimum Variance approach
        #   This class derives from the Strategy Class and implements the
        #   optimization problem associated to the Markowitz's theory with
        #   explicit diversification in the cost function 

    #Description: Relative importance of the variance.
    
    class obj:
        name = 'Equally Weighted Risk Contribution Strategy'
        pass

    
    """def __init__(self, name, lambda_value, delta_value):
        self.name = 'Diversified Mean Variance Strategy'
        self.lambda_value = 1 #Description: Relative importance of the variance
        self.delta_value = 1 #Description: Relative importance of the diversification
    """
    
    
    # Description: This function runs the corresponding strategy, fitting the model weights. 
    def solveOptimizationProblem(obj, data, vars):
        # Type: It returns the optimized weights
        # Compute numbers of data points and assets 
        (numElements, N) = data.shape
        # mean and covariance
        Sigma   = EmpiricalCovariance().fit(data).covariance_*12              # I use 12 for annualizing the covmatrix
        
        def func(w,Omega):
            x = 0
            R = Omega*w
            for i in range(1,len(w)):
                for j in range(1,len(w)):
                    x = x + (w(i)*R(i)-w(j)*R(j))**2
            x = x/(w*R)
            return x

        # Sequential Quadratic Programming
        #f = @(w) obj.func(w,Sigma)
        #func = lambda x: np.cos(14.5 * x - 0.3) + (x + 0.2) * x
        x0=[0.5]

        minimizer_kwargs = {"method": "BFGS"}
        ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs, niter=200)
        A = np.ones((1,N))
        b = 1
        lb = np.zeros((N,1))
        w0=1/N*np.ones((N,1))

        opts    = optimset( 'Display','off')
        
        W = fmincon(f,w0,[],[],A,b,lb,[],[],opts)
        return W

    def config(obj,data,vars, varsCV):
        
        return obj     

    
    """def func(obj,w,Omega):
        x = 0
        R = Omega*w
        for i in range(1,len(w)):
            for j in range(1,len(w)):
                x = x + (w(i)*R(i)-w(j)*R(j))**2
        x = x/(w*R)
        return x"""





