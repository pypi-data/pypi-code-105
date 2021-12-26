import flame_unsup.utils
import numpy as np
#from functools import partial #not needed
from flame_unsup.utils import scaleData, co_variance  #featurise is not needed

def dfeaturise(dat,dx,dy,method=co_variance):
    x,y,nv = dat.shape
    cm = []
    for i in range(int(x/dx)):
        cm.append([]) 
        for j in range(int(y/dy)):
            val = dat[i*dx:(i+1)*dx,j*dy:(j+1)*dy,:]
            cmj = method(val.reshape((-1,nv)))
            cm[i].append(cmj)        
    return np.array(cm)

def regionalSVD(cmo,index=0):
    ret = []
    for i,b in enumerate(cmo):
        u,S,V = np.linalg.svd(b,full_matrices=False)
        if index==0:
            ret[i].append([S,V])
        else:
            ret[i].append(V[0])
    return ret

def regionalFMM(cmo,vec): ## Helinger
    ret = []
    for i,b in enumerate(cmo):
        ret[i].append(np.sum(b*vec,axis=(0,1)))
    return np.array(ret)

def globalSVD(X,method=co_variance): ## Cosine
    cm_big = method(X)
    _,S,V = np.linalg.svd(cm_big,full_matrices=False)
    return V*S/S.max()

class Kurtosis():
    def __init__(self,method=co_variance):
        self.method = method
        self.order = 2

    def fit_predict(self, dat, nshape = 56):
        nx,ny,nv = mat.shape #here what does mat refer is it dat?
        # ndat,_ = normalDat(dat)
        ndat = scaleData(dat)  ## some features are ignored; see docs
        fdat = dfeaturise(ndat,dx=nshape,dy=nshape, method=self.method)
        cmo = fdat.reshape(-1,nv)
        vec = globalSVD(ndat.reshape(-1,nv))
        # cm1 = regionReduce(cmo,2)
        # sv1 = regionalSVD(cm1)
        fm1 = regionalFMM(cmo,vec)
        return fm1.reshape(nx,ny)

class Distance():
    def __init__(self,name="kurtosis"):
        self.n =0
        self.name = name
        self.__class__.__name__ = "DistancesUS" #self.__class__.__name__ is the name of the class
        
    def fit(self,X):
        self.vec = globalSVD(X)[0]
       
    def predict(self,X):
        y = 1- self.decision_function(X)
        yh = utils.MinMaxScalar(y)
        return  -2*np.array(yh >0.5,dtype=int) + 1
    
    def fit_predict(self,X):
        self.fit(X)
        
        return self.predict(X)
    
    def decision_function(self,X):
#         y = np.sum(X@self.vec,axis=1)
        y = X@self.vec
#         y = X@self.vec  #@ refers to matrix multiplication
        return y/y.max()
         
    
    
    
import sklearn

from sklearn.linear_model import LinearRegression #not needed?
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

from sklearn.metrics import mean_absolute_error,f1_score,roc_curve #mean_absolute_error,f1_score,roc_curve is not needed?
from sklearn.metrics import plot_confusion_matrix,plot_precision_recall_curve #both are not needed?




class Unsup():
    def __init__(self):
        ocs = OneClassSVM(nu=0.09)
        lof = LocalOutlierFactor(novelty=True)
        isf = IsolationForest(contamination=0.09)
        een = EllipticEnvelope()
        krt = Distance()    #doubt?
        self.clfs = [ocs, lof, isf, een,krt]
    
    def train(self,x,y=np.zeros(7),i=2):
        self.nx,self.ny,self.nv = x.shape
        self.xtrain = self.encode(x)
        self.ytrain = y.reshape(-1) #-1 means it is reshaped to 1d array
        self.ana = self.clfs[i]
        self.ana.fit(self.xtrain) #doubt?
    
    def encode(self,x):
        return x.reshape(-1,self.nv)
    
    def decode(self,y):
        return y.reshape(self.nx,self.ny)
    
    def dscore(self,x):
        ## scoring pattern is 
        ## 0==> Inliears
        ## 1==> anomaly
        x = self.encode(x)
        y = -self.ana.fit_predict(x)
        return self.decode((y+1)/2)
    
    def bscore(self,x):
        x = self.encode(x)
        y = self.ana.predict(x)
        y -= 1
        return self.decode(-y/2)
    
    def rscore(self,x):
        x = self.encode(x)
        y = -self.ana.decision_function(x)
        y -= y.min()
        return self.decode(y/y.max())
            
