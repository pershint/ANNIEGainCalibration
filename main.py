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
        leds_on = str(raw_input("Which LEDs are on (Input is CSV, least to greatest): "))
        led_PINs = str(raw_input("PIN setpoint for LEDs: "))
        fittype = str(raw_input("Fit type to perform (Gauss2, Gauss3): "))
        if fittype not in ["Gauss2","Gauss3"]:
            print("Please input a valid fitting approach to take.")
            sys.exit(0)
    with open(ap.DB) as dbfile:
        db = json.load(dbfile)
        fitdata = db[fittype]
        dbfile.close()

    #channel_list = np.arange(331,336,1)
    channel_list = np.array([356,357,360,364,365,367,368,370])

    GainFinder = gf.GainFinder(myfile)
    if(fittype == "Gauss2"):
        GainFinder.setFitFunction(fu.gauss2dep)
        GainFinder.setInitialFitParams(fu.gauss2depInitialParams)
        GainFinder.setBounds(fu.gauss2depLB,fu.gauss2depUB)
        print(fu.gauss2InitialParams)
    if(fittype == "Gauss3"):
        GainFinder.setFitFunction(fu.gauss3)
        GainFinder.setInitialFitParams(fu.gauss3InitialParams)
        GainFinder.setBounds(fu.gauss3LB,fu.gauss3UB)
    thehist_title = "hist_charge_CNUM" #FIXME: Make a configurable somehow
    #loop through each channel, show the histogram, and ask whether to use 
    #Default fitting params
    for channel_num in channel_list:
        print("FITTING FOR CHANNEL %i"%(channel_num))
        thehist = thehist_title.replace("CNUM",str(channel_num))
        if not myfile.GetListOfKeys().Contains(thehist):
            print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
            continue
        #First, try to fit the pedestal
        init_params = [10000,0.00001,0.0001]
        ped_fitrange = [0,0.0003]
        pedopt,pedcov,pedxdata,pedydata,pedyunc = GainFinder.FitPedestal(thehist,init_params,ped_fitrange)
        pl.PlotHistAndFit(pedxdata,pedydata,fu.gauss1,pedxdata,pedopt,"Gauss1")
        
        FitComplete = False
        while not FitComplete:
            UseDefault = str(raw_input("Use default fit parameters? [y/N]"))
            if UseDefault in ["y","Y","yes","Yes","YES"]:
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist)
            elif UseDefault in ["n","N","No","no","NO"]:
                InitialParams = pin.GetInitialParameters(fittype)
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist)
            print("BEST FIT PARAMS: " + str(popt))
            print("View your fit and close.")
            pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt,fittype)
            good_fit = str(raw_input("Happy with this fit? [y/N]: "))
            if good_fit in ["y","Y","yes","Yes","YES"]:
                FitComplete = True
            if popt is not None:
                FitComplete = True
        pl.PlotHistPEDAndPEs(xdata,ydata,pedopt,popt)
    #Since we've made it out, save to the DB
        db[fittype]["Channel"].append(channel_num)
        db[fittype]["RunNumber"].append(runnum)
        db[fittype]["LEDsOn"].append(leds_on)
        db[fittype]["LEDPINs"].append(led_PINs)
        db[fittype]["Date"].append(date)
        errs = np.sqrt(np.diag(pcov))
        if fittype in ["Gauss2","Gauss3"]:
            db[fittype]["c1Height"].append(popt[0])
            db[fittype]["c1Mu"].append(popt[1])
            db[fittype]["c1Sigma"].append(popt[2])
            db[fittype]["c2HScale"].append(popt[3])
            db[fittype]["c2MScale"].append(popt[4])
            db[fittype]["c2SScale"].append(popt[5])
            db[fittype]["c1Height_unc"].append(errs[0])
            db[fittype]["c1Mu_unc"].append(errs[1])
            db[fittype]["c1Sigma_unc"].append(errs[2])
            db[fittype]["c2HScale_unc"].append(errs[3])
            db[fittype]["c2MScale_unc"].append(errs[4])
            db[fittype]["c2SScale_unc"].append(errs[5])
        if fittype == "Gauss3":
            db[fittype]["c3HScale"].append(popt[6])
            db[fittype]["c3MScale"].append(popt[7])
            db[fittype]["c3SScale"].append(popt[8])
            db[fittype]["c3HScale_unc"].append(errs[6])
            db[fittype]["c3MScale_unc"].append(errs[7])
            db[fittype]["c3SScale_unc"].append(errs[8])
    with open(ap.DB,"w") as dbfile:
        json.dump(db,dbfile,sort_keys=False, indent=4)
