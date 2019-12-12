import numpy as np
import json
import ROOT
import sys

import lib.ArgParser as ap
import lib.Functions as fu
import lib.GainFinder as gf
import lib.ParamInput as pin
import lib.Plots as pl

if __name__=='__main__':
    print(" ###### WELCOME TO ANNIE LED PEAK FINDER ###### ")
    channel_list = np.arange(331,470,1)
    WM_list = np.array([382,393,404,405])
    HMWBLUXETEL_list = np.setdiff1d(channel_list,WM_list)
    
    HMWBLUXETELInitialParams = np.array([1000,450,6,1000,578,6,1000,750,6,1000,867,5])
    WMInitialParams = np.array([1000,780,6,1000,900,6,1000,1070,6,1000,1200,5])
    if ap.APPEND is not None:
        print(" ####### USING THIS FILE TO FIT LED PEAK TIMES ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)

    GainFinder = gf.GainFinder(myfile)
    GainFinder.setFitFunction(fu.gauss4)
    thehist_title = "hist_peaktime_CNUM" #FIXME: Make a configurable somehow
    #loop through each channel, show the histogram, and ask whether to use 
    #Default fitting params
    for channel_num in HMWBLUXETEL_list:
        thehist = thehist_title.replace("CNUM",str(channel_num))
        print("FITTING FOUR GAUSSIANS (C,m,s) TO PEAKTIME DISTRIBUTION")
        if not myfile.GetListOfKeys().Contains(thehist):
            print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
            continue
        GainFinder.setInitialFitParams(HMWBLUXETELInitialParams)
        popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
        print("BEST FIT PARAMS: " + str(popt))
        print("%i,%f,%f"%(channel_num,popt[1],popt[2]))
        print("%i,%f,%f"%(channel_num,popt[4],popt[5]))
        print("%i,%f,%f"%(channel_num,popt[7],popt[8]))
        print("%i,%f,%f"%(channel_num,popt[10],popt[11]))
        #pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt)
    
    for channel_num in WM_list:
        thehist = thehist_title.replace("CNUM",str(channel_num))
        print("FITTING FOUR GAUSSIANS (C,m,s) TO PEAKTIME DISTRIBUTION")
        if not myfile.GetListOfKeys().Contains(thehist):
            print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
            continue
        GainFinder.setInitialFitParams(HMWBLUXETELInitialParams)
        popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
        print("BEST FIT PARAMS: " + str(popt))
        print("%i,%f,%f"%(channel_num,popt[1],popt[2]))
        print("%i,%f,%f"%(channel_num,popt[4],popt[5]))
        print("%i,%f,%f"%(channel_num,popt[7],popt[8]))
        print("%i,%f,%f"%(channel_num,popt[10],popt[11]))
        #pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt)
