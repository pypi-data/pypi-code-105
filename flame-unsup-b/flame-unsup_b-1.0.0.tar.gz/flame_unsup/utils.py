## utilities used in kurtosis analysis
import numpy as np
import functools as fc

def MinMaxScalar(x):
    ## x is a one dimensional array 
    x  -= x.min()
    xmax = x.max()
    return x/xmax

def MeanMaxScalar(x):
    ## x is a feature set:
    x -= x.mean() #x should be a float array
    return x/x.max()

def ZeroMeanScalar(x):
    ## x is a one dimensional array 
    x -= x.mean() 
    vx = x.var()
    if vx == 0:
        print("Divide by zero Error")
    return x/vx

def NoScalar(x):
    return x/x.max()


def scaleData(tdat,scalar=ZeroMeanScalar,threshold=1e-11):
    ## input data usually has to be u
    ## so outermost index corresp to feat
    adat = []
    ignor = []
    for i,a in enumerate(tdat.T): #T is the transpose of array
        if featIgnore(a,eta=threshold):
            ignor.append(i)  ## ignore is decided using athresh
        else:
            adat.append(scalar(a))
    print("Ignored Features are",ignor)
    return np.array(adat).T

def co_variance(X,bias=0):
    nx,i = X.shape ## X is input data matrix # X.shape will return a tuple consisting of number of rows and columns, rows will be assigned       to nx and i will be assigned columns
    ans = np.zeros((i,i),dtype=float)
    for a in X:
        ans += np.outer(a,a)
    return ans/(nx-bias)

def ex_variance(cm):
    i,_ = cm.shape
    fv = np.outer(cm,cm)
    return fv.reshape(i**3,i)

def ra_kurtosis(X,bias=0):
    nx,i = X.shape
    ans = np.zeros((i**3,i))
    for a in X:
        ans += np.outer(np.outer(np.outer(a,a),a),a) #outer=u.transpose(v) where u,v are matrices
    return ans/(nx-bias)

def co_kurtosis(rand_mat,bias=0):
    ck = ra_kurtosis(rand_mat,bias)
    cm = co_variance(rand_mat,bias)
    ev = ex_variance(cm)
    return ck- 3*ev





### Pooling methods
def maxPool(cmi,fx=1):
    return cmi.max(axis=0) #axis=0 is columns

def vectorise(cmi,fx,moment=co_variance):
    ret = moment(cmi)
    u,S,V = np.linalg.svd(ret,full_matrices=False) #svd=u,s,v.T
    return V[0]*S[0]

twovector = fc.partial(vectorise,moment=co_variance) #not needed?
fourvector =  fc.partial(vectorise,moment=co_kurtosis) #not needed?
    
   
def maverages(cmi,fx):
    ret = cmi.sum(axis=0)
    return ret/fx

def preporcess(T,pool=12,scalar=ZeroMeanScalar,sampler=maverages):
    ## TO reduce the data to 12x12 grid size; 
    ### Improvements max pooling or avg pooling
    
    nx,ny,nv = T.shape
    if type(pool)==int:
        nfx = int(nx/pool)
        nfy = int(ny/pool)
    else:
        nfx,nfy = pool
    fdat = scaleData(T,scalar=scalar)
    ndat = featurise(fdat,fx=nfx,fy=nfy,sampler=sampler)
    nx,ny,nv = ndat.shape
#     x = ndat.reshape(-1,nv)
    return ndat



def featurise(cmo,fx=2,sampler=maverages,fy=0):
    x,y,nv, = cmo.shape
    cm = []
    if fy==0:
        fy = fx
    for i in range(int(x/fx)):
        cm.append([])
        for j in range(int(y/fy)):
            cmi = cmo[i*fx:(i+1)*fx,j*fy:(j+1)*fy,:].reshape((-1,nv))
            cm[i].append(sampler(cmi,fx))
    return np.array(cm)


def get_fmm(Vset,Set,Nf=2):
    features = []
    for i in range(Nf):
        fmm = 0.
        for s1,v1 in zip(Set,Vset):
            fmm += s1*v1[i]**2
        features.append(fmm/Set.sum())
    return features

def featIgnore(mat,eta = 1e-10):
    sentinel = False
    if abs(mat.max()-mat.min()) < eta:
        sentinel = True
    return sentinel
    