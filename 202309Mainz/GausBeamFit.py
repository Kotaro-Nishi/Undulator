import cv2
import matplotlib.pyplot as plt
import numpy as np

import scipy
from scipy.optimize import leastsq

from matplotlib.backends.backend_pdf import PdfPages

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

"""
plt.imshow(img)
plt.contour(f(prm,xx,yy))
plt.show()
"""



# create
pdfname = path[:-4] + ".pdf"
pdf = PdfPages(pdfname)
fig = plt.figure(figsize=(8.27,11.69), dpi=600)

plt.subplot(2,2,2)
plt.imshow(img)
plt.contour(f(prm,xx,yy))

ax1 = fig.add_subplot(2,2,3,projection="3d")
surf = ax1.plot_surface(xx, yy, f(prm,xx,yy), cmap='bwr', linewidth=0)

"""
ax2 = fig.add_subplot(4,2,2,projection="3d")
x_flat = xx.flatten()
y_flat = yy.flatten()
img_flat = img.flatten()
dx = np.ones_like(x_flat)
dy = np.ones_like(y_flat)
ax2.bar3d(x_flat,y_flat,0,1,1,img_flat)
"""
plt.subplot(2,2,1)
plt.axis('off')

label = ["Amplitude","x0","y0","xsigma","ysigma"]
table = [label,prm,np.sqrt(np.diag(cov))]
table = np.array(table).T
col_width = [0.2,0.4,0.4]
plt.table(cellText=table, colLabels= ("name","prm","error"),loc ='center',cellLoc ="center",colWidths=col_width)

pdf.savefig()
pdf.close()