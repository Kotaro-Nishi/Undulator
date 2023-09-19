import cv2
import matplotlib.pyplot as plt
import numpy as np

import scipy
from scipy.optimize import leastsq


path = "LaserPHnoAp750ms0005.TIF"
img = cv2.imread(path,cv2.IMREAD_UNCHANGED).astype(float)


def f(prm,x,y):
    amp = prm[0]
    a = prm[1]
    b = prm[2]
    sigA = prm[3]
    sigB = prm[4]
    return amp*np.exp( - ((x-a)/sigA)**2 - ((y-b)/sigB)**2 )


def chi(prm,x,y,img):
    d = f(prm,x,y) - img
    d = d.flatten()
    return d


x = np.arange(len(img))
y = np.arange(len(img[0]))
xx,yy  = np.meshgrid(x,y) 

"""
prm = (1000,100turn on0,1000,500,500)
img2 = f(prm,xx,yy)
plt.imshow(img2)
plt.show()
"""



init_val = (10000,1000,1000,1000,1000)
prm, cov, info, msg, ier = leastsq(chi,init_val,args=(xx,yy,img),full_output=True)

chi2 = np.sum(((f(prm,xx,yy)-img))**2)

for i in range(5):
    print("p{:} : {:10.5f} +- {:10.5f}".format(i,prm[i],np.sqrt(cov[i,i])))

plt.imshow(img)
plt.contour(f(prm,xx,yy))
plt.show()