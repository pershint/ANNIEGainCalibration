import json
import lib.ArgParser as ap
import lib.Functions as fu
import lib.GainFinder as gf
import lib.ParamInput as pin
import ROOT
import sys

if __name__=='__main__':
    print(" ###### WELCOME TO ANNIE GAIN CALIBRATION ###### ")
    if ap.APPEND is not None:
        print(" ####### APPENDING NEW INFO TO GAIN DATABASE ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)
        runnum = str(input("Input run number: "))
        date = str(input("Input date of run (MM/DD/YYYY): "))
        fittype = str(input("Fit type to perform (2Gauss, 3Gauss) "))
        if fittype not in ["2Gauss","3Gauss"]:
            print("Please input a valid fitting approach to take.")
            sys.exit(0)
    with open(ap.DB) as dbfile:
        db = json.load(dbfile)
        fitdata = db[fittype]

    channel_list = np.arange(331,336,1)

    GainFinder = gf.GainFinder(myfile)
    if(fittype == "Gauss2"):
        GainFinder.SetFitFunction(fu.gauss2)
        GainFinder.SetInitialParams(fu.gauss2InitialParams)
    if(fittype == "Gauss3"):
        GainFinder.SetFitFunction(fu.gauss3)
        GainFinder.SetInitialParams(fu.gauss3InitialParams)
    GainFinder.setHistString("hist_charges_CNUM") #FIXME: Make a configurable?
    #loop through each channel, show the histogram, and ask whether to use 
    #Default fitting params
    for channel in channel_list:
        thehist = self.hist_string.replace("CNUM",str(channel_num))
        if not myfile.GetListOfKeys().Contains(thehist):
            print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
            continue
        while not FitComplete:
            UseDefault = str(input("Use default fit parameters? [y/N]"))
            if UseDefault in ["y","Y","yes","Yes","YES"]:
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
            elif UseDefault in ["n","N","No","no","NO"]:
                InitialParams = pin.GetInitialParameters(fittype)
                popt,pcov,xdata,ydata,y_unc = GainFinder.FitHistogram(thehist)
            pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt)
    print(runnum)
    print(date)
    print(fittype)
