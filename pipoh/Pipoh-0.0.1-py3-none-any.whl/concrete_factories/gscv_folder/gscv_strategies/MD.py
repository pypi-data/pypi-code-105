from numpy import array, dot
from qpsolvers import solve_qp
import bayes_opt
from bayes_opt import BayesianOptimization
import statistics
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

class MD:
    def __init__(self, data):
        self.data = []
    pass
    
    #The Equally Weighted Minimum Variance approach
        #   This class derives from the Strategy Class and implements the
        #   optimization problem associated to the Markowitz's theory with
        #   explicit diversification in the cost function 

    #Description: Relative importance of the variance.
    
    class obj:
        name = 'Maximum Diversification Strategy'
        pass


    
    
    # Description: This function runs the corresponding strategy, fitting the model weights. 
    def solveOptimizationProblem(obj, data, vars):
        # Type: It returns the optimized weights
        # Compute numbers of data points and assets 
        (numElements, N) = data.shape
        # mean and covariance
        Sigma   = EmpiricalCovariance().fit(data).covariance_*12              # I use 12 for annualizing the covmatrix
        Vars    = np.diag(Sigma)                                              # variances of the stocks
        Stds    = np.sqrt(Vars)                                # mean log returns
        

        H = 2*(lambdaValue*Sigma)
        f = - mu.H #FALTA TRANSPOSE

        Aeq     = np.ones((1,N))
        beq     = 1
        LB      = np.zeros((1,N))                                         
        UB      = np.ones((1,N))                                                     
        #opts    = optimset('Algorithm', 'interior-point-convex', 'Display','off')
        #   Revisar cómo meter la opción de 'interior-point-convex'

        # Python reference for quadprog: 
        #   https://pypi.org/project/qpsolvers/
        #Original funct (it contains opts) (Wa, varP)  = solve_qp(H,f,[],[],Aeq,beq,LB,UB,UB/N,opts) 
        
        P=H
        q=np.asarray(f).reshape((6,))
        G=np.zeros((6,6))
        h=np.zeros(6)
        A=np.asarray(Aeq).reshape((6,))
        b=np.array([beq])
        lb=LB
        ub=UB
        
        from numpy import array, dot
        from qpsolvers import solve_qp

        """M = array([[1., 2., 0.], [-8., 3., 2.], [0., 1., 1.]])
        P = dot(M.T, M)  # this is a positive definite matrix
        q = dot(array([3., 2., 3.]), M).reshape((3,))
        G = array([[1., 2., 1.], [2., 0., 1.], [-1., 2., -1.]])
        h = array([3., 2., -2.]).reshape((3,))
        A = array([1., 1., 1.])
        b = array([1.])"""

        #(Wa, varP, third_parameter) = solve_qp(P, q, G, h, A, b)


        (Wa, varP, third_parameter,fourth_parameter,fifth_parameter,sixt_parameter)  = solve_qp(P, q, G, h, A, b)
        
        W = deltaValue* Wa + (1-deltaValue)*(1/N)*np.ones((N,1))
        
        return W
    
    def config(obj,data,vars, varsCV):
        

        
        return obj     

    

    def func(obj,w2,StandardDev,CovMatrix):
        x=-(statistics.stdev(w2.H))/(w2'*CovMatrix*w2)**(-.5)
        return value





