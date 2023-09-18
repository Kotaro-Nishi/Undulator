#### Enter file path ####
from tkinter import *
import cv2
import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from numpy import transpose as nptp

"""
arg =sys.argv
path = arg[1]

img = cv2.imread(path,cv2.IMREAD_UNCHANGED)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.imshow(img,cmap='flag')
plt.show()
"""
img =None

def load_button():
    global img
    button1['text'] = 'Loaded'
    path = d_entry.get() + f_entry.get()
    print(str(path))
    axA.cla()
    axH.cla()
    axW.cla()
    try:
        status.set("Progress")
        img = cv2.imread(path,cv2.IMREAD_UNCHANGED).astype(float)
        axA.imshow(img,cmap='flag')
        fig_canvasA.draw()
        axW.plot(img[0],lw=0.3,label = 0)
        axW.legend()
        fig_canvasW.draw()
        
        axH.plot(nptp(img)[0],range(len(nptp(img)[0])),lw=0.3,label =0)
        axH.legend()
        axH.invert_yaxis()
        fig_canvasH.draw()

        status.set("Success")
    except Exception as e:
        status.set(e)
        print(e)
        button1['text'] = 'Loda Tif'

def HV_apply():
    try:
        hol_idx = int(h_entry.get())
        hol_str.set(h_entry.get())
    except:
        hol_idx = 0
    try:
        ver_idx = int(v_entry.get())
        ver_str.set(v_entry.get())
    except:
        ver_idx = 0
    try:
        axW.plot(img[ver_idx],lw=0.3,label=ver_idx)
        axW.legend()
        fig_canvasW.draw()
        axH.plot(nptp(img)[hol_idx],range(len(nptp(img)[hol_idx])),lw=0.3,label=hol_idx)
        axH.legend()
        fig_canvasH.draw()
    except Exception as e:
        status.set(e)

def Refresh():
    axH.cla()
    axW.cla()
    axH.plot()
    axH.invert_yaxis()
    axW.plot()
    fig_canvasW.draw()
    fig_canvasH.draw()

def defaultpath():
    d_entry.delete(0,END)
    f_entry.delete(0,END)
    d_entry.insert(END,'/data/Mainz/BeamEnergyCalib/data/Beam20200320_1/Energymeasurement_2/raw_shortExp/')
    f_entry.insert(END,'File1.tif')

def BGpath():
    d_entry.delete(0,END)
    f_entry.delete(0,END)
    d_entry.insert(END,'/data/Mainz/BeamEnergyCalib/data/Beam20200320_1/Energymeasurement_2/BG/raw_shortExp/') 
    f_entry.insert(END,'File1.tif')

def HGpath():
    d_entry.delete(0,END)
    f_entry.delete(0,END)
    d_entry.insert(END,'/data/Mainz/BeamEnergyCalib/data/Beam20200320_1/Energymeasurement_2/HG/Mercury202003202154/Spectrum/Pos0/') 
    f_entry.insert(END,'img_000000000_Default_000.tif') 

def finish():
    root.destroy()


if __name__ =='__main__':
    root = Tk()
    
    #window
    root.title("Tif viewer")
    root.geometry('1200x725')
    root.resizable(False,False)

    #frame
    frame1 = Frame(root,width = 1200, height = 25) 
    frame2 = Frame(root,width = 1200, height = 25)
    frameA = Frame(root,width = 600,  height = 350)
    frameH = Frame(root,width = 400,  height = 350)
    frameW = Frame(root,width = 600,  height = 300)
    frameS = Frame(root,width = 400,  height = 300)
    frameC = Frame(root,width =400, height = 25)

    frame1.propagate(False)
    frame2.propagate(False)
    frameA.propagate(False)
    frameW.propagate(False)
    frameH.propagate(False)
    frameS.propagate(False)
    frameC.propagate(False)

    frame1.grid(row=0,column=0,columnspan=2)
    frame2.grid(row=1,column=0,columnspan=2)
    frameA.grid(row=2,column = 0)
    frameH.grid(row=2,column = 1)
    frameW.grid(row=3,column = 0)
    frameS.grid(row=3,column = 1)
    frameC.grid(row=4,column = 1)

    #widget  
  
    ##frame 1 load file path
    d_entry = Entry(frame1,width=100)
    d_label = Label(frame1,text='dir')
    f_label = Label(frame1,text='file')
    f_entry = Entry(frame1,width =10)

    path = StringVar()
    button1 = Button(frame1,text='Load Tif',command = load_button)
   
    d_label.pack(side=LEFT)
    d_entry.pack(side =LEFT)
    f_label.pack(side= LEFT)
    f_entry.pack(side = LEFT)
    button1.pack(side = LEFT)
    
    

    ##frame 2 message
    status = StringVar()
    label_status =Label(frame2,textvariable=status)
    label_status.pack()

    #plot
    figA = Figure()
    axA = figA.add_subplot(1,1,1)
    fig_canvasA = FigureCanvasTkAgg(figA,frameA)
    toolbarA = NavigationToolbar2Tk(fig_canvasA,frameA)
    fig_canvasA.get_tk_widget().pack(fill=BOTH,expand=False)

    figH = Figure()
    axH = figH.add_subplot(1,1,1)
    fig_canvasH = FigureCanvasTkAgg(figH,frameH)
    toolbarH = NavigationToolbar2Tk(fig_canvasH,frameH)
    fig_canvasH.get_tk_widget().pack(fill=BOTH,expand=False)

    figW = Figure()
    axW = figW.add_subplot(1,1,1)
    fig_canvasW = FigureCanvasTkAgg(figW,frameW)
    toolbarW = NavigationToolbar2Tk(fig_canvasW,frameW)
    fig_canvasW.get_tk_widget().pack(fill=BOTH,expand=False)

    ##default
    

    ##frame S summarizer
    hol_idx = 0
    ver_idx = 0
    hol_str =StringVar()
    hol_str.set(0)
    ver_str = StringVar()
    ver_str.set(0)
    h_title=Label(frameS,text="Set holizontal px")
    v_title=Label(frameS,text="Set vertical px")
    h_entry = Entry(frameS,width=8)
    v_entry = Entry(frameS,width=8)
    hol_label =Label(frameS,textvariable = hol_str)
    ver_label= Label(frameS,textvariable = ver_str)
    s_button = Button(frameS,text='Apply',command =HV_apply)
    refrech_button =Button(frameS,text='Refresh',command = Refresh)

    h_title.grid(row = 0,column=0)
    h_entry.grid(row =0, column=1)
    hol_label.grid(row =0, column=2)
    v_title.grid(row=1,column=0)
    v_entry.grid(row =1, column=1)
    ver_label.grid(row =1, column=2)
    s_button.grid(row =2, column=0)
    refrech_button.grid(row =2, column=1)

    ## frameC summarizer
    button_finish =Button(frameC, text='FINISH',command =finish)
    button_finish.pack(side = RIGHT)

    #menu
    menubar = Menu(root)
    filemenu = Menu(menubar,tearoff=0)
    filemenu.add_command(label ="data",command = defaultpath)
    filemenu.add_command(label ="BG",command = BGpath)
    filemenu.add_command(label= 'HG',command = HGpath)
    
    menubar.add_cascade(label ="data path",menu = filemenu)

    root.config(menu=menubar)
    root.mainloop()

