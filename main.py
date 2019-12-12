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
    print(" ###### WELCOME TO ANNIE GAIN CALIBRATION ###### ")
    if ap.APPEND is not None:
        print(" ####### APPENDING NEW INFO TO GAIN DATABASE ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)
        runnum = str(raw_input("Input run number: "))
        date = str(raw_input("Input date of run (MM/DD/YYYY): "))
        fittype = str(raw_input("Fit type to perform (Gauss2, Gauss3): "))
        if fittype not in ["Gauss2","Gauss3"]:
            print("Please input a valid fitting approach to take.")
            sys.exit(0)
    with open(ap.DB) as dbfile:
        db = json.load(dbfile)
        fitdata = db[fittype]

    channel_list = np.arange(331,336,1)

    GainFinder = gf.GainFinder(myfile)
    if(fittype == "Gauss2"):
        GainFinder.setFitFunction(fu.gauss2)
        GainFinder.setInitialFitParams(fu.gauss2InitialParams)
        print(fu.gauss2InitialParams)
    if(fittype == "Gauss3"):
        GainFinder.setFitFunction(fu.gauss3)
        GainFinder.setInitialFitParams(fu.gauss3InitialParams)
    thehist_title = "hist_charge_CNUM" #FIXME: Make a configurable somehow
    #loop through each channel, show the histogram, and ask whether to use 
    #Default fitting params
    for channel_num in channel_list:
        thehist = thehist_title.replace("CNUM",str(channel_num))
        if not myfile.GetListOfKeys().Contains(thehist):
            print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
            continue
        FitComplete = False
        while not FitComplete:
            UseDefault = str(raw_input("Use default fit parameters? [y/N]"))
            if UseDefault in ["y","Y","yes","Yes","YES"]:
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
            elif UseDefault in ["n","N","No","no","NO"]:
                InitialParams = pin.GetInitialParameters(fittype)
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
            if popt is not None:
                FitComplete = True
            print("BEST FIT PARAMS: " + str(popt))
            pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt)
    print(runnum)
    print(date)
    print(fittype)
