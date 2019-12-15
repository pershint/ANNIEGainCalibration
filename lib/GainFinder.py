import scipy.optimize as scp
import numpy as np
import Functions as fu
import copy

class GainFinder(object):
    def __init__(self, ROOTFile):
        self.ROOTFile = ROOTFile
        self.initial_params = []
        self.hist_string = "hist_charge_CNUM"

        self.ped_mean = None
        self.ped_sigma = None
        self.ped_fit_y = None
        self.ped_fit_x = None

        self.fitfunc = None
        self.lower_bounds = None
        self.upper_bounds = None


    def setFitFunction(self,fitfunc):
        self.fitfunc = fitfunc
    
    def setInitialFitParams(self,initial_params):
        self.initial_params =  initial_params

    def setBounds(self,lower_bounds,upper_bounds):
        self.lower_bounds =  lower_bounds
        self.upper_bounds =  upper_bounds

    def FitPedestal(self,HistName,init_params,fit_range):
        '''
        Uses a Gaussian from the Functions library to attempt to fit
        the pedestal peak of the distribution.  A fit range can be
        given if helping down-select to the pedestal-dominant region.

        Inputs:

        HistName [string]
            string of histogram name in self.ROOTFile.

        init_params [array]
            Initial parameters to try fitting a single gaussian with.
            Format is [amplitude,mean,sigma].

        fit_range [array]
            Range of values to perform fit across.  Helps to down-select
            to the ped-only range.
        '''
        print("FITTING TO PEDESTAL NOW")
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        ped_indices = []
        for i in xrange(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            if len(fit_range)>0:
                if ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)) <fit_range[0]):
                    continue
                if ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)) >fit_range[1]):
                    continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        try:
            popt, pcov = scp.curve_fit(fu.gauss1, bin_centers, evts, p0=init_params, maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
            popt = None
            pcov = None
            return popt, pcov, bin_centers, evts, evts_unc
        self.ped_fit_x = bin_centers
        self.ped_fit_y =fu.gauss1(self.ped_fit_x,popt[0],popt[1],popt[2]) 
        self.ped_mean = popt[1]
        self.ped_sigma = popt[2]
        return popt, pcov, bin_centers,evts,evts_unc

    def FitPEPeaks(self,HistName,exclude_ped = True, subtract_ped = False):
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        for i in xrange(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            if exclude_ped is True and ((float(thehist.GetBinWidth(i))/2.0) + \
                    float(thehist.GetBinLowEdge(i)) < (self.ped_mean + 7*self.ped_sigma)):
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        if subtract_ped == True:
            #Subtract off the pedestal
            ped_sub_evts = copy.deepcopy(evts)
            ped_sub_evts_unc = copy.deepcopy(evts_unc)

            #Need to subtract across pedestal fit range
            ped_start_ind = np.where(bin_centers == min(self.ped_fit_x))[0]
            for i,b in enumerate(self.ped_fit_x):
                ped_sub_evts[ped_start_ind+i] = ped_sub_evts[ped_start_ind+i] - self.ped_fit_y[i]
                #FIXME: Also want to correct for uncertainty in fit
            evts = ped_sub_evts
            evts_unc = ped_sub_evts_unc

        try:
            if self.lower_bounds is None or self.upper_bounds is None:
                popt, pcov = scp.curve_fit(self.fitfunc, bin_centers, evts, p0=self.initial_params, maxfev=6000)
            else:
                popt, pcov = scp.curve_fit(self.fitfunc, bin_centers, evts, p0=self.initial_params,
                      bounds=(self.lower_bounds,self.upper_bounds),maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT AFTER ITERATIONS...")
            popt = None
            pcov = None
        return popt, pcov, bin_centers, evts, evts_unc
