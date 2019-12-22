import numpy as np
import json
import ROOT
import sys

import lib.ArgParser as ap
import lib.Functions as fu
import lib.GainFinder as gf
import lib.ParamInput as pin
import lib.Plots as pl

LEDMAP = {0:5, 1:28, 2:6, 3:10}

if __name__=='__main__':
    print(" ###### WELCOME TO ANNIE LED PEAK FINDER ###### ")
    channel_list = np.arange(331,470,1)
    WM_list = np.array([382,393,404,405])
    HMWBLUXETEL_list = np.setdiff1d(channel_list,WM_list)

    HMWBLUXETELInitialParams = [np.array([100,450,6,6]),np.array([100,578,6,6]),
                     np.array([100,750,6,6]),np.array([100,867,5,6])]
    HMWBLUXETELLB = [np.array([0,410,0,0]),np.array([0,550,0,0]),
                     np.array([0,720,0,0]),np.array([0,840,0,0])]
    HMWBLUXETELUB = [np.array([1E4,490,15,15]),np.array([1E5,600,15,15]),
                     np.array([1E4,780,15,15]),np.array([1E5,900,15,15])]
    WMInitialParams = [np.array([100,780,6,6]),np.array([100,900,6,6]),
                      np.array([100,1070,6,6]),np.array([100,1200,5,5])]
    WMLB = [np.array([0,750,0,0]),np.array([0,870,0,0]),
                      np.array([0,1040,0,0]),np.array([0,1170,0,0])]
    WMUB = [np.array([1E4,810,10,10]),np.array([1E4,930,10,10]),
                      np.array([1E4,1100,10,10]),np.array([1E4,1230,10,10])]

    #HMWBLUXETELInitialParams = [np.array([1000,450,6]),np.array([1000,578,6]),
    #                 np.array([1000,750,6]),np.array([1000,867,5])]
    #HMWBLUXETELLB = [np.array([0,410,0]),np.array([0,550,0]),
    #                 np.array([0,720,0]),np.array([0,840,0])]
    #HMWBLUXETELUB = [np.array([1E4,490,15]),np.array([1E5,600,15]),
    #                 np.array([1E4,780,15]),np.array([1E5,900,15])]


    #WMInitialParams = [np.array([1000,780,6]),np.array([1000,900,6]),
    #                  np.array([1000,1070,6]),np.array([1000,1200,5])]
    #WMLB = [np.array([0,750,0]),np.array([0,870,0]),
    #                  np.array([0,1040,0]),np.array([0,1170,0])]
    #WMUB = [np.array([1E4,810,10]),np.array([1E4,930,10]),
    #                  np.array([1E4,1100,10]),np.array([1E4,1230,10])]
    if ap.APPEND is not None:
        print(" ####### USING THIS FILE TO FIT LED PEAK TIMES ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)

    GainFinder = gf.GainFinder(myfile)
    GainFinder.setFitFunction(fu.landau)
    thehist_title = "hist_peaktime_CNUM" #FIXME: Make a configurable somehow
    #loop through each channel, show the histogram, and ask whether to use 
    #Default fitting params
    results = {"channel":[], "LED":[], "mu":[], "mu_unc":[]}
    missing = {"channel":[], "LED":[]}
    for channel_num in HMWBLUXETEL_list:
        for j in range(4):
            thehist = thehist_title.replace("CNUM",str(channel_num))
            print("FITTING FOUR GAUSSIANS (C,m,s) TO PEAKTIME DISTRIBUTION")
            if not myfile.GetListOfKeys().Contains(thehist):
                print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
                continue
            GainFinder.setInitialFitParams(HMWBLUXETELInitialParams[j])
            GainFinder.setBounds(HMWBLUXETELLB[j],HMWBLUXETELUB[j])
            popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist, 
                    exclude_ped = False, subtract_ped = False,
                    fit_range = [HMWBLUXETELLB[j][1],HMWBLUXETELUB[j][1]])
            if type(popt) != np.ndarray:
                print("CHANNEL %i PEAK %i FAILED TO FIT"%(channel_num,j))
                missing["channel"].append(channel_num)
                missing["LED"].append(LEDMAP[j])
                continue
            pcovd = np.diag(pcov)
            pl.PlotHistAndFit(xdata,ydata,fu.landau,xdata,popt,"Landau")
            print("BEST FIT PARAMS: " + str(popt))
            if np.sqrt(pcovd[1]) > 15:
                print("CHANNEL %i PEAK %i HAS CRITICAL UNC. ON MEAN"%(channel_num,j))
                missing["channel"].append(channel_num)
                missing["LED"].append(LEDMAP[j])
                continue
            print("%i,%f,%f,%f,%f"%(channel_num,popt[1],popt[2],np.sqrt(pcovd[1]),
                np.sqrt(pcovd[2])))
            if (np.sqrt(pcovd[1]) < 15):
                results["channel"].append(channel_num)
                results["LED"].append(LEDMAP[j])
                results["mu"].append(popt[1])
                results["mu_unc"].append(np.sqrt(pcovd[1]))
    
    for channel_num in WM_list:
        for k in range(4):
            thehist = thehist_title.replace("CNUM",str(channel_num))
            print("FITTING FOUR GAUSSIANS (C,m,s) TO PEAKTIME DISTRIBUTION")
            if not myfile.GetListOfKeys().Contains(thehist):
                print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
                continue
            GainFinder.setInitialFitParams(WMInitialParams[j])
            GainFinder.setBounds(WMLB[j],WMUB[j])
            popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist, 
                    exclude_ped = False, subtract_ped = False,
                    fit_range = [WMLB[j][1],WMUB[j][1]])
            if type(popt) != np.ndarray:
                print("CHANNEL %i PEAK %i FAILED TO FIT"%(channel_num,k))
                missing["channel"].append(channel_num)
                missing["LED"].append(LEDMAP[j])
                continue
            pcovd = np.diag(pcov)
            print("BEST FIT PARAMS: " + str(popt))
            if np.sqrt(pcovd[1]) > 15:
                print("CHANNEL %i PEAK %i HAS CRITICAL UNC. ON MEAN"%(channel_num,j))
                missing["channel"].append(channel_num)
                missing["LED"].append(LEDMAP[j])
                continue
            print("%i,%f,%f,%f,%f"%(channel_num,popt[1],popt[2],np.sqrt(pcovd[1]),
                np.sqrt(pcovd[2])))
            if (np.sqrt(pcovd[1]) < 15):
                results["channel"].append(channel_num)
                results["LED"].append(LEDMAP[j])
                results["mu"].append(popt[1])
                results["mu_unc"].append(np.sqrt(pcovd[1]))
            #pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt)
    with open("PeakFitResults.json","w") as f:
        json.dump(results,f,indent=4)
    with open("MissingPeaks.json","w") as f:
        json.dump(missing,f,indent=4)

