import numpy as np
import scipy as sp
import Functions as fu
import copy
import scipy.optimize as scp

#Class that estimates the SPE charge using a model-independent calculation
# from arXiv:1602.03150v1.  Generally you need background data (LEDs off) for 
#Each voltage setpoint to use this approach.  Instead, we will estimate the
#No-PE flashes using a fit to the pedestal and assume we can neglect dark 
#Noise. to
#ANNIE PMT Charge distributions

class FermiFitter(object):
    def __init__(self,ROOTFile):
        print("INITIALIZING FERMIFITTER CLASS")
        self.ROOTFile = ROOTFile
        
        self.ped_fit_x = None
        self.ped_fit_y = None
        self.ped_fit_y_unc = None
        self.ped_mean = None
        self.ped_sigma = None 

    def ProcessHistogram(self,HistName):
        '''For the loaded ROOTFile, Returns a single ROOT histogram's bin data in
        numpy array format.

        Input:
            HistName [string]
            Name of histogram to process into numpy arrays

        Output:
            bin_centers,bin_values,bin_value_uncertainties
        '''
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        fit_bin_centers, fit_evts,fit_evts_unc =(), (), () #pandas wants ntuples
        ped_indices = []
        for i in xrange(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        hist_data = {'bins': bin_centers, 'bin_heights': evts,
                'bin_height_uncs':evts_unc}

        return hist_data

    def _EstimatePedestalTotal(self,hist_data):
        '''Estimates the total number of triggers in data that have zero PE.
        Zero PE entries are modeled as a gaussian plus an exponential tail.
        '''
        back_pedestal_ind = np.where(hist_data['bins'] < self.ped_mean + 1*self.ped_sigma)[0]
        back_pedestal = np.sum(hist_data['bin_heights'][back_pedestal_ind])
        front_pedestal_ind = np.where(hist_data['bins'] >=(self.ped_mean + 1*self.ped_sigma))[0]
        front_pedestal = np.sum(self.ped_fit_y[front_pedestal_ind])
        pedestal_estimate =np.sum(back_pedestal) + np.sum(front_pedestal)
        return pedestal_estimate

    def _GetPedestalModel(self,hist_data):
        '''Estimates the total number of triggers in data that have zero PE.
        Zero PE entries are modeled as a gaussian plus an exponential tail.
        '''
        back_pedestal_ind = np.where(hist_data['bins'] < self.ped_mean)[0]
        back_pedestal = hist_data['bin_heights'][back_pedestal_ind]
        front_pedestal_ind = np.where(hist_data['bins'] >=self.ped_mean)[0]
        front_pedestal = self.ped_fit_y[front_pedestal_ind]
        pedestal_model =np.concatenate((back_pedestal,front_pedestal))
        return pedestal_model

    def _EstimateOccupancy(self,hist_data):
        '''Estimates the occupancy of the PMT.  Occupancy is defined as the
        number of triggers with at least one PE.  Estimation of the pedestal 
        (0 PE events) is done as follows:
        1 - occupancy = sum(bins up to the pedestal mean) + sum(best fit
        to pedestal and pedestal tail beyond the mean)
        '''
        if self.ped_fit_y is None:
            print("NO PEDESTAL FIT!  You must run FitPedestal first.")
            return -99999
        pedestal_estimate = self._EstimatePedestalTotal(hist_data)
        print("PEDESTAL TOTAL ESTIMATE: " + str(pedestal_estimate))
        total_triggers = np.sum(hist_data['bin_heights'])
        print("TOTAL TRIG ESTIMATE: " + str(total_triggers))
        print("OCCUPANCY ESTIMATE: " + str(-np.log((pedestal_estimate/total_triggers))))

        return -np.log((pedestal_estimate/total_triggers))

    def EstimateSPEMean(self,hist_data):
        if self.ped_fit_y is None:
            print("NO PEDESTAL FIT!  You must run FitPedestal first.")
            return -99999
        #mean_total = np.average(hist_data['bins'])
        #mean_pedestal = np.average(self._EstimatePedestal(hist_data))
        mean_total = fu.WeightedMean(hist_data['bins'],hist_data['bin_heights'])
        mean_pedestal = fu.WeightedMean(hist_data['bins'],self._GetPedestalModel(hist_data))
        print("TOTAL MEAN: " + str(mean_total))
        print("PEDESTAL MEAN: " + str(mean_pedestal))
        #Now, we estimate the photon occupancy distribution; modeled as poisson
        occ = self._EstimateOccupancy(hist_data)
        ##occupancy is the mean of the photon distribution
        mean_photon_distribution = occ

        return ((mean_total - mean_pedestal)/mean_photon_distribution)



    def FitPedestal(self,hist_data,init_params,fit_range,fit_tail=False,exp_fit_range=[]):
        '''
        Uses a Gaussian from the Functions library to attempt to fit
        the pedestal peak of the distribution.  A fit range can be
        given if helping down-select to the pedestal-dominant region.

        Inputs:

        hist_data [dict]
            Ouput dictionary from the ProcessHistogram method.

        init_params [array]
            Initial parameters to try fitting a single gaussian with.
            Format is [amplitude,mean,sigma].

        fit_range [array]
            Range of values to perform fit across.  Helps to down-select
            to the ped-only range.
        '''
        print("FITTING TO PEDESTAL NOW")
        bin_centers = hist_data["bins"]
        evts = hist_data["bin_heights"]
        evts_unc = hist_data["bin_height_uncs"]
        fit_bin_centers = copy.deepcopy(bin_centers)
        fit_evts = copy.deepcopy(evts)
        fit_evts_unc = copy.deepcopy(evts_unc)
        if len(fit_range)>0:
            fit_bin_inds = np.where((bin_centers > fit_range[0]) & (bin_centers < fit_range[1]))[0]
            fit_bin_centers = fit_bin_centers[fit_bin_inds]
            fit_evts = fit_evts[fit_bin_inds]
            fit_vts_unc = fit_evts_unc[fit_bin_inds]
        print("TRYING INITIAL PARAMS: " + str(init_params))
        try:
            popt, pcov = scp.curve_fit(fu.gauss1, bin_centers, evts, p0=init_params, maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
            popt = None
            pcov = None
            return popt, pcov, bin_centers, evts, evts_unc
        self.ped_fit_x = bin_centers
        self.ped_fit_y =fu.gauss1(self.ped_fit_x,popt[0],popt[1],popt[2])
        perr = np.diag(pcov)
        self.ped_fit_y_unc =abs(fu.gauss1(self.ped_fit_x,popt[0]+perr[0],popt[1],popt[2]+perr[2]) - 
                               fu.gauss1(self.ped_fit_x,popt[0]-perr[0],popt[1],popt[2]-perr[2]))
        self.ped_mean = popt[1]
        self.ped_sigma = popt[2]
        #self.ped_fit_y =fu.OrderStat(self.ped_fit_x,popt[0],popt[1],popt[2],popt[3]) 
        #self.ped_mean = popt[2]
        #self.ped_sigma = popt[3]
        if fit_tail is True:
            exp_ind = []
            if len(exp_fit_range) > 0:
                exp_ind = np.where((bin_centers > exp_fit_range[0]) & (bin_centers < exp_fit_range[1]))[0]
            else:
                exp_ind = np.where((bin_centers > self.ped_mean+ 1*self.ped_sigma) & (bin_centers < self.ped_mean + 4*self.ped_sigma))[0]
            exp_bins = bin_centers[exp_ind]
            exp_evts = evts[exp_ind] #- self.ped_fit_y[exp_ind]
            exp_evts_unc = evts_unc[exp_ind]
            #exp_init_params = [popt[0]/popt[2],popt[2],10*popt[1]]
            #exp_init_params = [exp_evts[0],popt[2],10*popt[1]]
            exp_init_params = [popt[0],popt[2],10*popt[1]]
            print("EXPONENTIAL FIT: INIT PARAMS: " + str(exp_init_params))
            try:
                eopt, ecov = scp.curve_fit(lambda x,D,tau,t: fu.gaussPlusExpo(x,popt[0],popt[1],popt[2],D,tau,t), 
                        exp_bins, exp_evts, p0=exp_init_params, sigma=exp_evts_unc, maxfev=12000)
                #eopt, ecov = scp.curve_fit(lambda x,D,tau,t: D*np.exp(-(x-t)/tau), 
                #        exp_bins, exp_evts, p0=exp_init_params, maxfev=12000)
            except RuntimeError:
                print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
                popt = None
                pcov = None
                return popt, pcov, bin_centers, evts, evts_unc
            popt = np.concatenate((popt,eopt))
            #
            self.ped_fit_y =fu.gaussPlusExpo(self.ped_fit_x,popt[0],popt[1],
                    popt[2],eopt[0],eopt[1],eopt[2]) 
        return popt, pcov, self.ped_fit_y, self.ped_fit_y_unc
