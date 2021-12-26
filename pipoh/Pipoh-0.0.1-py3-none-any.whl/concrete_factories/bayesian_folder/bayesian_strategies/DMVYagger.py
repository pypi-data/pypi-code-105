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


#Bayesian libraries
import numpy as np
from pyGPGO.covfunc import squaredExponential
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.GPGO import GPGO
class DMVYagger:
    def __init__(self, data):
        self.data = []
    pass
    
    #The Equally Weighted Minimum Variance approach
        #   This class derives from the Strategy Class and implements the
        #   optimization problem associated to the Markowitz's theory with
        #   explicit diversification in the cost function 

    #Description: Relative importance of the variance.
    
    class obj:
        name = 'Diversified Mean Variance Yagger Strategy'
        lambda_value = 1 #Description: Relative importance of the variance
        delta_value = 1 #Description: Relative importance of the diversification
        pass

    
    """def __init__(self, name, lambda_value, delta_value):
        self.name = 'Diversified Mean Variance Yagger Strategy'
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
        Vars    = np.diag(Sigma)                                              # variances of the stocks
        mu      = data.mean(axis=0).H*12                                      # mean log returns
            
        if False==hasattr(vars,'lambda_value'):
            # third parameter does not exist, so default it to something
            lambdaValue = DMVYagger.obj.lambda_value
        else:
            lambdaValue = vars.lambda_value
        
        
        if False==hasattr(vars,'delta'):
            # third parameter does not exist, so default it to something
            deltaValue = DMVYagger.obj.delta_value
        else:
            deltaValue = vars.delta_value
        
        
        H = 2*(lambdaValue*Sigma + deltaValue*np.eye(N))
        f = -mu.H-(deltaValue*2*((1/N)*np.ones((1,N))))

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



        #(Wa, varP, third_parameter,fourth_parameter,fifth_parameter,sixt_parameter)  = solve_qp(P, q, G, h, A, b)
        W=np.array(solve_qp(P, q, G, h, A, b)) 
        #W = deltaValue* Wa + (1-deltaValue)*(1/N)*np.ones((N,1))
        
        return W
    
    def config(obj,data,vars, varsCV):
        
        from Strategy import rollingWindowsValidation
        
        
        # Create the validation set
        dataValidation = data[0:-vars.validationWindows:,:]
        # Compute the CV windows
        varsCV.validationWindows = vars.CVWindows
        # Create the optimization variable
        
        sexp = squaredExponential()
        gp = GaussianProcess(sexp)
        acq = Acquisition(mode='ExpectedImprovement')
        param = {'lambda_value': ('cont', [0,1]), 'deltaValue': ('cont', [0,1])}
        #param es equivalente en MATLAB a:
        #   num = WLBC.obj.lambda_value
        #   ub = WLBC.obj.lowerBound
        #Bayesian optimization:
        def errorLoss(lambda_value, deltaValue):
            vars.lambda_value = lambda_value
            vars.deltaValue = deltaValue
            returns = rollingWindowsValidation(obj, dataValidation, varsCV)
            value = np.std(returns)/returns.mean()
            return value
        
        results = GPGO(gp, acq, errorLoss, param)
        results.run(max_iter=1)
        #Extract the best parameters
        #obj.lambda_value = results.best[[0]]
        #obj.lowerBound = results.best[[1]]
        obj.lambda_value =results.getResult()[0]['lambda_value']
        obj.deltaValue =results.getResult()[0]['deltaValue']
        #obj.lambda_value = 0.99
        #obj.lowerBound = 0.3128
        
        return obj     

    

    def errorLoss(obj,dataValidation, vars, lambda_value, delta_value):
        vars.lambda_value = lambda_value
        vars.delta_value = delta_value
        returns = rollingWindowsValidation(obj, dataValidation, vars)
        value = np.std(returns)/returns.mean()
        return value





