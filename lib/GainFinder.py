import scipy.optimize as scp

class GainFinder(object):
    def __init__(self, ROOTFile):
        self.ROOTFile = ROOTFile
        self.hist_string = "hist_charge_CNUM"
        self.fitfunc = None
        self.initial_params = []

    def setHistString(self,hist_string):
        '''Set the name of the histograms that will have fits performed on them.
           Place CNUM where the channel number is defined in the string.  
           Example: setHistString("hist_charge_CNUM")
           '''
           self.hist_string = hist_string

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
        popt, pcov = scp.curve_fit(self.fitfunc, bin_centers, evts, p0=self.initial_params,
                     sigma=evts_unc,maxfev=6000)
        return popt, pcov, bin_centers, evts, evts_unc
