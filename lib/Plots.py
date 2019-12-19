import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import Functions as fu
import numpy as np

sns.set(font_scale=1.4)

def PlotHistAndFit(xdata,ydata,function,xfit,params,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    print("POPT GOING INTO FUNC: " + str(params))
    if fittype=="Gauss1" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="GaussPlusExpo" and params is not None:
        yfit = fu.gauss1(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
        yfit2 = fu.expo(xfit,params[3],params[4],params[5])
        plt.plot(xfit,yfit2,marker='None')
    if fittype=="Gauss3" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    if (fittype=="Gauss2") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    plt.xlabel("x data")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of data and fit to data")
    plt.show()

def PlotPedestal(xdata,ydata,function,xfit,params,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    print("POPT GOING INTO FUNC: " + str(params))
    if fittype=="OrderStatPlusExpo" and params is not None:
        yfit = fu.OrderStat(xfit,params[0],params[1],params[2],
                params[3])
        plt.plot(xfit,yfit,marker='None')
        yfit2 = fu.expo(xfit,params[4],params[5],params[6])
        plt.plot(xfit,yfit2,marker='None')
    if fittype=="Gauss1" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="GaussPlusExpo" and params is not None:
        yfit = fu.gauss1(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
        yfit2 = fu.expo(xfit,params[3],params[4],params[5])
        plt.plot(xfit,yfit2,marker='None')
    if fittype=="Gauss3" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    if (fittype=="Gauss2") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
    if (fittype=="SPE2Peaks") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5],params[6],params[7],params[8],
                params[9],params[10])
        plt.plot(xfit,yfit,marker='None')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Fit of pedestal and failedamplification hits to data")
    plt.show()

def PlotHistPEDAndPEs(xdata,ydata,pedparams,peparams,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    yped = fu.gauss1(xdata,pedparams[0],pedparams[1],pedparams[2])
    plt.plot(xdata,yped,marker='None',label='Pedestal')
    print("PEDPARAMS ARE: " + str(pedparams))
    if len(pedparams>3):
        yexp = fu.expo(xdata,pedparams[3],pedparams[4],pedparams[5])
        plt.plot(xdata,yexp,marker='None',label='Partial amp. hits')
    y1spe = fu.gauss1(xdata,peparams[0],peparams[1],peparams[2])
    plt.plot(xdata,y1spe,marker='None',label='1PE')
    y2spe = fu.gauss1(xdata,peparams[3]*peparams[0],peparams[4]*peparams[1],peparams[5]*peparams[2])
    plt.plot(xdata,y2spe,marker='None',label='2PE')
    if fittype == "Gauss3":
       y3spe = fu.gauss1(xdata,(peparams[3]**2)*peparams[0],(peparams[4]**2)*peparams[1],(peparams[5]**2)*peparams[2])
       plt.plot(xdata,y3spe,marker='None',label='3PE')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of ped, PE distribution fits to data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()

def PlotHistPEDAndPEs_V2(xdata,ydata,pedparams,peparams,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    yped = fu.gauss1(xdata,pedparams[0],pedparams[1],pedparams[2])
    if len(pedparams>3):
        exp_range = np.where(xdata>pedparams[1])[0]
        yexp = fu.expo(xdata[exp_range],pedparams[3],pedparams[4],pedparams[5])
        plt.plot(xdata[exp_range],yexp,marker='None',label='Partial amp. hits')
    plt.plot(xdata,yped,marker='None',label='Pedestal')
    if fittype=="SPE" or fittype=="SPE2Peaks":
        y1spe = fu.SPEGaussians_NoExp(xdata,peparams[0],peparams[1],peparams[2],peparams[3],peparams[4],
                peparams[5])
        plt.plot(xdata,y1spe,marker='None',label='1PE')
    if fittype=="SPE2Peaks":
        y2spe = fu.SPEGaussians_NoExp(xdata,peparams[6]*peparams[0],peparams[7]*peparams[1],
                peparams[8]*peparams[2],peparams[3],peparams[4],peparams[5])
        plt.plot(xdata,y2spe,marker='None',label='2PE')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of ped, PE distribution fits to data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()
