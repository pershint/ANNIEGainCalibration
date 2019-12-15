import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
