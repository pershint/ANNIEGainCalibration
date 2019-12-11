import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def PlotHistAndFit(self,xdata,ydata,function,xfit,params):
    plt.plot(xdata,ydata,marker="none")
    yfit = function(xfit,params)
    plt.plot(xfit,yfit)
    plt.xlabel("x data")
    plt.ylabel("Entries")
    plt.title("Comparison of data and fit to data")
    plt.show()
