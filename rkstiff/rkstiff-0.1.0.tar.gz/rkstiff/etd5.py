
from rkstiff.etd import ETDCS,phi1,phi2,phi3
import numpy as np
from typing import Callable
from scipy.linalg import expm

class _ETD5_Diagonal:
    """
    ETD5 diagonal system strategy for ETD5 solver 
    """
    def __init__(self,linop,NLfunc,contourM,contourR,modecutoff):
        self.linop = linop
        self.NLfunc = NLfunc
        self.M = contourM
        self.R = contourR
        self.modecutoff = modecutoff
        
        N = linop.shape[0]
        self._EL14, self._EL12, self._EL34, self._EL = [\
                np.zeros(N,dtype=np.complex128) for _ in range(4)]
        self._a21, self._a31, self._a32, self._a41, self._a43, self._a51,\
                self._a52,self._a54, self._a61, self._a62, self._a63,\
                self._a64, self._a65 = [np.zeros(N,dtype=np.complex128) for _ in range(13)]   
        self._b1, self._b3, self._b4,self._b5,self._b6 = [\
                np.zeros(N,dtype=np.complex128) for _ in range(5)]   
        self._NL1, self._NL2, self._NL3,self._NL4, self._NL5,\
                self._NL6 = [np.zeros(N,dtype=np.complex128) for _ in range(6)]
        self._k = np.zeros(N,dtype=np.complex128)
        
    def _updateCoeffs(self,h):
        z = h*self.linop
        # diagonal system -> L is 1D array (of independent modes)
        self._EL14 = np.exp(z/4.0)
        self._EL12 = np.exp(z/2.0)
        self._EL34 = np.exp(3.0*z/4.0)
        self._EL = np.exp(z)

        smallmode_idx = np.abs(z) < self.modecutoff
        # compute big mode coeffs
        zb = z[~smallmode_idx] # z big
        phi1_14 = h*phi1(zb/4)
        phi2_14 = h*phi2(zb/4)
        phi1_12 = h*phi1(zb/2)
        phi2_12 = h*phi2(zb/2)
        phi1_34 = h*phi1(3*zb/4)
        phi2_34 = h*phi2(3*zb/4)
        phi1_1 = h*phi1(zb)
        phi2_1 = h*phi2(zb)
        phi3_1 = h*phi3(zb)

        self._a21[~smallmode_idx] = phi1_14/4.
        self._a31[~smallmode_idx] = (phi1_14-phi2_14/2.)/4.
        self._a32[~smallmode_idx] = phi2_14/8.
        self._a41[~smallmode_idx] = (phi1_12 - phi2_12)/2.
        self._a43[~smallmode_idx] = phi2_12/2.
        self._a51[~smallmode_idx] = 3.0*(phi1_34 - 3.*phi2_34/4.)/4.0
        self._a52[~smallmode_idx] = -3*phi1_34/8.
        self._a54[~smallmode_idx] = 9*phi2_34/16.
        self._a61[~smallmode_idx] = (-77*phi1_1+59*phi2_1)/42.
        self._a62[~smallmode_idx] = 8*phi1_1/7.
        self._a63[~smallmode_idx] = (111*phi1_1-87*phi2_1)/28.
        self._a65[~smallmode_idx] = (-47*phi1_1+143*phi2_1)/84.
        self._b1[~smallmode_idx] = 7*(257*phi1_1 - 497*phi2_1 + 270*phi3_1)/2700
        # Paper has error in b3 phi2 coefficient (states this is 497 but it is actually 467)
        self._b3[~smallmode_idx] = (1097*phi1_1 - 467*phi2_1 - 150*phi3_1)/1350
        self._b4[~smallmode_idx] = 2*(-49*phi1_1 + 199*phi2_1 - 135*phi3_1)/225
        self._b5[~smallmode_idx] = (-313*phi1_1 + 883*phi2_1 - 90*phi3_1)/1350
        self._b6[~smallmode_idx] = (509*phi1_1 - 2129*phi2_1 + 1830*phi3_1)/2700
        
        # compute small mode coeffs
        zs = z[smallmode_idx] # z small
        r = self.R*np.exp(2j*np.pi*np.arange(0.5,self.M)/self.M)
        rr, zz = np.meshgrid(r,zs)
        Z = zz+rr
        
        phi1_14 = h*np.sum(phi1(Z/4),axis=1)/self.M
        phi2_14 = h*np.sum(phi2(Z/4),axis=1)/self.M
        phi1_12 = h*np.sum(phi1(Z/2),axis=1)/self.M
        phi2_12 = h*np.sum(phi2(Z/2),axis=1)/self.M
        phi1_34 = h*np.sum(phi1(3*Z/4),axis=1)/self.M
        phi2_34 = h*np.sum(phi2(3*Z/4),axis=1)/self.M
        phi1_1 = h*np.sum(phi1(Z),axis=1)/self.M
        phi2_1 = h*np.sum(phi2(Z),axis=1)/self.M
        phi3_1 = h*np.sum(phi3(Z),axis=1)/self.M
         
        self._a21[smallmode_idx] = phi1_14/4.
        self._a31[smallmode_idx] = (phi1_14-phi2_14/2.)/4.
        self._a32[smallmode_idx] = phi2_14/8.
        self._a41[smallmode_idx] = (phi1_12 - phi2_12)/2.
        self._a43[smallmode_idx] = phi2_12/2.
        self._a51[smallmode_idx] = 3.0*(phi1_34 - 3.*phi2_34/4.)/4.0
        self._a52[smallmode_idx] = -3*phi1_34/8.
        self._a54[smallmode_idx] = 9*phi2_34/16.
        self._a61[smallmode_idx] = (-77*phi1_1+59*phi2_1)/42.
        self._a62[smallmode_idx] = 8*phi1_1/7.
        self._a63[smallmode_idx] = (111*phi1_1-87*phi2_1)/28.
        self._a65[smallmode_idx] = (-47*phi1_1+143*phi2_1)/84.
        self._b1[smallmode_idx] = 7*(257*phi1_1 - 497*phi2_1 + 270*phi3_1)/2700
        # Paper has error in b3 phi2 coefficient (states this is 497 but it is actually 467)
        self._b3[smallmode_idx] = (1097*phi1_1 - 467*phi2_1 - 150*phi3_1)/1350
        self._b4[smallmode_idx] = 2*(-49*phi1_1 + 199*phi2_1 - 135*phi3_1)/225
        self._b5[smallmode_idx] = (-313*phi1_1 + 883*phi2_1 - 90*phi3_1)/1350
        self._b6[smallmode_idx] = (509*phi1_1 - 2129*phi2_1 + 1830*phi3_1)/2700

    def _N1_init(self,u):
        """ Initialize N1 before first call to updateStages """
        self._NL1 = self.NLfunc(u)
       
    def _updateStages(self,u):        
        """ One passthrough of RK solver for diagonal system """
        self._k = self._EL14*u + self._a21*self._NL1
        self._NL2 = self.NLfunc(self._k)
        self._k = self._EL14*u + self._a31*self._NL1 + self._a32*self._NL2
        self._NL3 = self.NLfunc(self._k)
        self._k = self._EL12*u + self._a41*self._NL1 + self._a43*self._NL3
        self._NL4 = self.NLfunc(self._k)
        self._k = self._EL34*u + self._a51*self._NL1 + self._a52*(self._NL2 - self._NL3) \
                               + self._a54*self._NL4
        self._NL5 = self.NLfunc(self._k)
        self._k = self._EL*u + self._a61*self._NL1 + self._a62*(self._NL2 - 3*self._NL4/2.0) \
                             + self._a63*self._NL3 + self._a65*self._NL5
        self._NL6 = self.NLfunc(self._k) 
        self._k = self._EL*u + self._b1*self._NL1 + self._b3*self._NL3 + self._b4*self._NL4 \
                             + self._b5*self._NL5 + self._b6*self._NL6
        self._NL1 = self._NL6 # FSAL principle
        return self._k

class _ETD5_NonDiagonal:
    """ ETD5 non-diagonal system strategy for ETD5 solver """
    def __init__(self,linop,NLfunc,contourM,contourR):
        self.linop = linop
        self.NLfunc = NLfunc
        self.M = contourM
        self.R = contourR
        
        N = linop.shape[0]
        self._EL14, self._EL12, self._EL34, self._EL = [np.zeros(shape=linop.shape,dtype=np.complex128) for _ in range(4)]
        self._a21, self._a31, self._a32, self._a41, self._a43, self._a51,\
                self._a52,self._a54, self._a61, self._a62, self._a63,\
                self._a64, self._a65 = [np.zeros(shape=linop.shape,dtype=np.complex128) for _ in range(13)]   
        self._b1, self._b3, self._b4,self._b5, self._b6 = [\
                np.zeros(shape=linop.shape,dtype=np.complex128) for _ in range(5)]   
        self._NL1, self._NL2, self._NL3,self._NL4, self._NL5,\
                self._NL6 = [np.zeros(N,dtype=np.complex128) for _ in range(6)]
        self._k = np.zeros(N,dtype=np.complex128)
        
    def _updateCoeffs(self,h):   
        # Update RK coefficients for 'matrix' np.array operator linop
        z = h*self.linop
        # Use expm matrix exponential function from scipy
        self._EL14 = expm(z/4.0)
        self._EL12 = expm(z/2.0)
        self._EL34 = expm(3.0*z/4.0)
        self._EL = expm(z)

        # Use contour integral evaluation for psi etd functions
        contour_points = self.R*np.exp(2j*np.pi*np.arange(0.5,self.M)/self.M)
        phi1_14,phi2_14,phi1_12,phi2_12,phi1_34,phi2_34 = [\
                np.zeros(shape=self.linop.shape,dtype=np.complex128) for _ in range(6)]
        phi1_1,phi2_1,phi3_1 = [np.zeros(shape=self.linop.shape,dtype=np.complex128) for _ in range(3)]

        for point in contour_points:
            Q14 = np.linalg.inv(point*np.eye(*self.linop.shape)-z/4.)
            Q12 = np.linalg.inv(point*np.eye(*self.linop.shape)-z/2.)
            Q34 = np.linalg.inv(point*np.eye(*self.linop.shape)-3*z/4.)
            Q = np.linalg.inv(point*np.eye(*self.linop.shape)-z)
            phi1_14 += point*phi1(point)*Q14/self.M
            phi2_14 += point*phi2(point)*Q14/self.M
            phi1_12 += point*phi1(point)*Q12/self.M
            phi2_12 += point*phi2(point)*Q12/self.M
            phi1_34 += point*phi1(point)*Q34/self.M
            phi2_34 += point*phi2(point)*Q34/self.M
            phi1_1 += point*phi1(point)*Q/self.M
            phi2_1 += point*phi2(point)*Q/self.M
            phi3_1 += point*phi3(point)*Q/self.M  
        

        self._a21 = h*phi1_14/4.
        self._a31 = h*(phi1_14-phi2_14/2.)/4.
        self._a32 = h*phi2_14/8.
        self._a41 = h*(phi1_12 - phi2_12)/2.
        self._a43 = h*phi2_12/2.
        self._a51 = h*3.0*(phi1_34 - 3.*phi2_34/4.)/4.0
        self._a52 = -3*h*phi1_34/8.
        self._a54 = h*9*phi2_34/16.
        self._a61 = h*(-77*phi1_1+59*phi2_1)/42.
        self._a62 = h*8*phi1_1/7.
        self._a63 = h*(111*phi1_1-87*phi2_1)/28.
        self._a65 = h*(-47*phi1_1+143*phi2_1)/84.
        self._b1 = h*7*(257*phi1_1 - 497*phi2_1 + 270*phi3_1)/2700
        self._b3 = h*(1097*phi1_1 - 467*phi2_1 - 150*phi3_1)/1350
        self._b4 = h*2*(-49*phi1_1 + 199*phi2_1 - 135*phi3_1)/225
        self._b5 = h*(-313*phi1_1 + 883*phi2_1 - 90*phi3_1)/1350
        self._b6 = h*(509*phi1_1 - 2129*phi2_1 + 1830*phi3_1)/2700

    def _N1_init(self,u):
        """ Initialize N1 before first call to updateStages """
        self._NL1 = self.NLfunc(u)
        
    def _updateStages(self,u):        
        self._k = self._EL14.dot(u) + self._a21.dot(self._NL1)
        self._NL2 = self.NLfunc(self._k)
        self._k = self._EL14.dot(u) + self._a31.dot(self._NL1) + self._a32.dot(self._NL2)
        self._NL3 = self.NLfunc(self._k)
        self._k = self._EL12.dot(u) + self._a41.dot(self._NL1) + self._a43.dot(self._NL3)
        self._NL4 = self.NLfunc(self._k)
        self._k = self._EL34.dot(u) + self._a51.dot(self._NL1) + self._a52.dot(self._NL2 - self._NL3) \
                               + self._a54.dot(self._NL4)
        self._NL5 = self.NLfunc(self._k)
        self._k = self._EL.dot(u) + self._a61.dot(self._NL1) + self._a62.dot(self._NL2 - 3*self._NL4/2.0) \
                             + self._a63.dot(self._NL3) + self._a65.dot(self._NL5)
        self._NL6 = self.NLfunc(self._k)
        self._k = self._EL.dot(u) + self._b1.dot(self._NL1) + self._b3.dot(self._NL3) + self._b4.dot(self._NL4) \
                             + self._b5.dot(self._NL5) + self._b6.dot(self._NL6)
        self._NL1 = self._NL6 # FSAL principle
        return self._k


class ETD5(ETDCS):
    """
    Exponential time-differencing constant step solver of 4th order (Krogstad)

    ATTRIBUTES
    __________

    linop : np.array
    NLfunc : function
    t : time-array stored with evolve function call 
    u : output-array stored with evolve function call 
    logs : array of info stored related to the solver

    ETD Parameters (see ETDAS class in etd module)
    ______________
    modecutoff : float
    contour_points :  int
    contour_radius : float 

    """
    
    def __init__(self,linop : np.ndarray,NLfunc : Callable[[np.ndarray],np.ndarray],\
            modecutoff : float = 0.01, contour_points : int = 32,\
            contour_radius : float = 1.0):
        """
        INPUTS
        ______

        linop : np.array
            Linear operator (L) in the system dtU = LU + NL(U). Can be either a 2D numpy array (matrix)
            or a 1D array (diagonal system). L can be either real-valued or complex-valued.

        NLfunc : function 
            Nonlinear function (NL(U)) in the system dtU = LU + NL(U). Can be a complex or real-valued function.

        diagonalize : bool, optional
            Diagonalize the linear operator (matrix) and solve the diagonalized system 

        ETDCS variables: modecutoff, contour_points, contour_radius (see ETDAS documentation from etd module)

        """
        super().__init__(linop,NLfunc,modecutoff=modecutoff,\
                contour_points=contour_points,contour_radius=contour_radius)
        self._method = None
        if self._diag:
            self._method = _ETD5_Diagonal(linop,NLfunc,self.contour_points,\
                    self.contour_radius,self.modecutoff)
        else:
            self._method = _ETD5_NonDiagonal(linop,NLfunc,self.contour_points,\
                    self.contour_radius)
        self.__N1_init = False

    def _reset(self):
        """ Resets solver to its initial state  """
        self.__N1_init = False
        self._h_coeff = None

    def _updateCoeffs(self,h):
        """ Update coefficients if step size h changed """
        if h == self._h_coeff:
            return
        self._h_coeff = h
        self._method._updateCoeffs(h)
        self.logs.append("ETD5 coefficients updated")
        
    def _updateStages(self,u,h):
        """ Computes u_{n+1} from u_{n} in one RK passthrough """
        self._updateCoeffs(h)
        if not self.__N1_init:
            self._method._N1_init(u)
            self.__N1_init = True
        return self._method._updateStages(u)

