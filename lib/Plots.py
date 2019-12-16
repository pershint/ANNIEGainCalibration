import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import Functions as fu
sns.set(font_scale=1.4)

def PlotHistAndFit(xdata,ydata,function,xfit,params,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    print("POPT GOING INTO FUNC: " + str(params))
    if fittype=="Gauss1" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="Gauss3" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5],params[6],params[7],params[8])
        plt.plot(xfit,yfit,marker='None')
    if (fittype=="Gauss2" or fittype=="GaussPlusExpo") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    plt.xlabel("x data")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of data and fit to data")
    plt.show()

def PlotHistPEDAndPEs(xdata,ydata,pedparams,peparams):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    yped = fu.gauss1(xdata,pedparams[0],pedparams[1],pedparams[2])
    plt.plot(xdata,yped,marker='None',label='Pedestal')
    y1spe = fu.gauss1(xdata,peparams[0],peparams[1],peparams[2])
    plt.plot(xdata,y1spe,marker='None',label='1PE')
    y2spe = fu.gauss1(xdata,peparams[3]*peparams[0],peparams[4]*peparams[1],peparams[5]*peparams[2])
    plt.plot(xdata,y2spe,marker='None',label='2PE')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of ped, 1PE, and 2PE fits to data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()
