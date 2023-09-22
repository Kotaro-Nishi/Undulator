import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import plot
from matplotlib.pyplot import show

from numpy.fft import fft as FFT
from numpy.fft import ifft as IFFT
from numpy.fft import fftshift as SHIFT

import scipy
from scipy.optimize import least_squares

import cv2

import sys

path = sys.argv[1]
img = cv2.imread(path,cv2.IMREAD_UNCHANGED).astype(float)


global N,a,wl,k
N = 2304
wl = 405e-9  # 波長（400nm）
D = 0.015 #サンプリング領域の大きさ
k = 2*np.pi /wl

def plane(x, y,amp,ap_x0,ap_y0,ap_rx,ap_ry):
    #global ap_x0,ap_y0,ap_rx,ap_r
    if abs(x - ap_x0) < ap_rx and abs(y-ap_y0) < ap_ry:
        return amp
    else:
        return 0

#X,Y = np.meshgrid(np.linspace(0,D,num = N),np.linspace(0,D,num = N))
Pv = np.vectorize(plane)
#Z = Pv(X, Y,ap_x0,ap_y0,ap_rx,ap_ry)

def AS2D(Z,z):
    NZ = np.zeros((2*N,2*N))
    NZ[int(N/2):int(N*3/2),int(N/2):int(N*3/2)] = Z
    plt.imshow(NZ)
    U = np.fft.fft2(NZ)
    
    k_x = np.fft.fftfreq(2*N,d = D/N) * 2 * np.pi
    k_y = np.fft.fftfreq(2*N,d= D/N) * 2 * np.pi
    K_X, K_Y = np.meshgrid(k_x, k_y)
    k_z = np.sqrt(k**2 - K_X**2 - K_Y**2)
    U_angular = np.fft.ifft2(U * np.exp(1.0j * k_z * z))
    
    I_angular = np.abs(U_angular)**2
    return I_angular[int(N/2):int(N*3/2),int(N/2):int(N*3/2)] 

def resid(prm,img):
    X,Y = np.meshgrid(np.linspace(0,D,num = N),np.linspace(0,D,num = N))
    Z = Pv(X,Y,prm[0],prm[2]*D/N,prm[3]*D/N,prm[4]*D/N,prm[5]*D/N)
    U = AS2D(Z,prm[1])
    res = U - img 
    res = res.flatten()
    return res

init_prm = (100,0.65,1140,1235,232,438)
result = least_squares(resid,init_prm,args = [img],diff_step= (0.1,0.001,0.05,0.05,0.05,0.05), verbose=2)

print(result)

