import scipy.optimize as scp
import numpy as np

class GainFinder(object):
    def __init__(self, ROOTFile):
        self.ROOTFile = ROOTFile
        self.initial_params = []
        self.hist_string = "hist_charge_CNUM"
        self.fitfunc = None


    def setFitFunction(self,fitfunc):
        self.fitfunc = fitfunc
    
    def setInitialFitParams(self,initial_params):
        self.initial_params =  initial_params

    def FitHistogram(self,HistName):
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        for i in xrange(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        try:
            popt, pcov = scp.curve_fit(self.fitfunc, bin_centers, evts, p0=self.initial_params,
                         maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT AFTER ITERATIONS...")
            return np.ones(12)*-9999, None,None,None,None
        return popt, pcov, bin_centers, evts, evts_unc
