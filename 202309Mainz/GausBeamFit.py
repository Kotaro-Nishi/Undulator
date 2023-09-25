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

init_val = (10000,1000,1000,1000,1000)
prm, cov, info, msg, ier = leastsq(chi,init_val,args=(xx,yy,img),full_output=True)
chi2 = np.sum(((f(prm,xx,yy)-img))**2)

for i in range(5):
    print("p{:} : {:10.5f} +- {:10.5f}".format(i,prm[i],np.sqrt(cov[i,i])))

fit = f(prm,xx,yy)


# create
pdfname = path[:-4] + ".pdf"
pdf = PdfPages(pdfname)
fig = plt.figure(figsize=(8.27,11.69), dpi=600)

plt.rcParams['font.size'] = 14

px_tick = np.linspace(0,2304,6)
px_ticklabel = np.arange(0,16,3)

plt.subplot2grid((3,2),(0,0),colspan=2)
plt.axis('off')
label = ["Amplitude",r"$x_0$ [mm]",r"$y_0$ [mm]",r"$\sigma_x$ [mm]",r"$\sigma_y$ [mm]"]
prm_format = ["{:.5f}".format(item*15/2304) for item in prm]
cov_format = ["{:.5f}".format(np.sqrt(item)) for item in np.diag(cov)]
table = [label,prm_format,cov_format]
table = np.array(table).T
col_width = [0.3,0.35,0.35]
tab = plt.table(cellText=table, colLabels= ("name","prm","error"),loc ='center',cellLoc ="right",colWidths=col_width)
tab.auto_set_font_size(False)
tab.set_fontsize(16)
tab.scale(0.8,1.6)


plt.subplot(3,2,3)
plt.title("2D plot")
im = plt.imshow(img)
plt.contour(fit)
plt.xticks(px_tick,px_ticklabel) 
plt.yticks(px_tick,px_ticklabel) 
plt.colorbar(im)
plt.xlabel(r"$p_x$ [mm]")
plt.ylabel(r"$p_y$ [mm]")


plt.subplot(3,2,4)
plt.title(r"holizontal plot : $p_x$ = {:.3f}".format(prm[2]/2304*15))
plt.plot(img[:][int(prm[2])],label = "data",linewidth=0.1)
plt.plot(fit[:][int(prm[2])],label = "fit",linewidth =0.3)
plt.legend()
plt.xlabel(r"$p_y$ [mm]")
plt.xticks(px_tick,px_ticklabel) 


plt.subplot(3,2,5)
plt.title(r"vertical plot : $p_y$ = {:.3f}".format(prm[1]/2304*15))
plt.plot(img[int(prm[1])],label = "data",linewidth=0.1)
plt.plot(fit[int(prm[1])],label = "fit",linewidth =0.3)
plt.legend()
plt.xlabel(r"$p_x$ [mm]")
plt.xticks(px_tick,px_ticklabel) 


ax2 = fig.add_subplot(3,2,6,projection="3d")
ax2.plot_surface(xx, yy, img, cmap='bwr', linewidth=0)
plt.xticks(px_tick,px_ticklabel) 
plt.yticks(px_tick,px_ticklabel) 
ax2.contour3D(xx,yy,fit)
ax2.set_zlim(0,prm[0])
plt.xticks(px_tick,px_ticklabel) 
plt.yticks(px_tick,px_ticklabel) 
plt.xlabel(r"$p_x$ [mm]")
plt.ylabel(r"$p_y$ [mm]")


plt.subplots_adjust(wspace =0.4 ,hspace = 0.4)
pdf.savefig()
pdf.close()

fit = fit.astype(np.uint16)
tif_path = path[:-4]+"_FIT.TIF"
cv2.imwrite(tif_path,fit)