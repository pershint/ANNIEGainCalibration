import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def PlotHistAndFit(xdata,ydata,function,xfit,params):
    plt.plot(xdata,ydata,linestyle='None')
    print("POPT GOING INTO FUNC: " + str(params))
    print("XFIT DATA POINTS: " + str(xfit))
    yfit = function(xfit,params)
    plt.plot(xfit,yfit,markerstyle='None')
    plt.xlabel("x data")
    plt.ylabel("Entries")
    plt.title("Comparison of data and fit to data")
    plt.show()
