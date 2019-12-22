import numpy as np
import json
import ROOT
import sys
import matplotlib.pyplot as plt

import lib.ArgParser as ap
import lib.Functions as fu
import lib.GainFinder as gf
import lib.ParamInput as pin
import lib.Plots as pl

HIST_TITLETEMPLATE = "hist_charge_CNUM" #FIXME: Make a configurable somehow
#loop through each channel, show the histogram, and ask whether to use 
#Default fitting params


if __name__=='__main__':
    print(" ###### WELCOME TO ANNIE GAIN CALIBRATION ###### ")
    if ap.APPEND is not None:
        print(" ####### APPENDING NEW INFO TO GAIN DATABASE ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)
        fittype = str(raw_input("Fit type to perform to PE peaks (Gauss2, Gauss3,SPE,SPE2Peaks,SPE3Peaks): "))
        if fittype not in ["Gauss2","Gauss3","SPE","SPE2Peaks","SPE3Peaks"]:
            print("Please input a valid fitting approach to take.")
            sys.exit(0)
    with open(ap.DB) as dbfile:
        db = json.load(dbfile)
        fitdata = db[fittype]
        dbfile.close()

    #FIXME: have this be a configurable or a file path added by user
    with open("./DB/TranspChannels.txt","r") as f:
        chans = f.readlines()
        for j,l in enumerate(chans):
            chans[j]=int(chans[j].rstrip("\n"))
    channel_list = np.array(chans)
    channel_list = np.arange(331,470)

    #Load dictionary of initial fit parameters
    with open("./DB/InitialParams.json","r") as f:
        init_params = json.load(f)


    if ap.FIT == "Simple":
        #Initialize Gain-Fitting class
        GainFinder = gf.GainFinder(myfile)
        if(fittype == "Gauss2"):
            GainFinder.setFitFunction(fu.gauss2dep)
            GainFinder.setInitialFitParams(init_params["GaussDepInitParams"])
            GainFinder.setBounds(init_params["GaussDepLB"],init_params["GaussDepUB"])
        if(fittype == "Gauss3"):
            GainFinder.setFitFunction(fu.gauss3dep)
            GainFinder.setInitialFitParams(init_params["GaussDepInitParams"])
            GainFinder.setBounds(init_params["GaussDepLB"],init_params["GaussDepUB"])
        if(fittype == "SPE"):
            GainFinder.setFitFunction(fu.SPEGaussians_NoExp)
            GainFinder.setInitialFitParams(init_params["SPEInitParams"])
            GainFinder.setBounds(init_params["SPELB"],init_params["SPEUB"])
        if(fittype == "SPE2Peaks"):
            GainFinder.setFitFunction(fu.SPE2Peaks)
            GainFinder.setInitialFitParams(init_params["SPE2PeaksInitParams"])
            GainFinder.setBounds(init_params["SPE2PeaksLB"],init_params["SPE2PeaksUB"])
        if(fittype == "SPE3Peaks"):
            GainFinder.setFitFunction(fu.SPE3Peaks)
            GainFinder.setInitialFitParams(init_params["SPE3PeaksInitParams"])
            GainFinder.setBounds(init_params["SPE3PeaksLB"],init_params["SPE3PeaksUB"])


        #Loop through channels in file and fit gains to each
        for channel_num in channel_list:
            print("FITTING FOR CHANNEL %i"%(channel_num))
            thehist = HIST_TITLETEMPLATE.replace("CNUM",str(channel_num))
            if not myfile.GetListOfKeys().Contains(thehist):
                print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
                continue
           

            #Fit photoelectron peaks
            FIT_TAIL = False
            FitComplete = False
            PedFitComplete = False
            GoodPedFit = False
            exp_fit_range = []
            while not PedFitComplete:
                #Fit pedestal and exponential tail from failed dynode hits
                print("PEDESTAL PARAMS: " + str(init_params["PedParams"]))
                pedopt,pedcov,pedxdata,pedydata,pedyunc = GainFinder.FitPedestal(
                        thehist, init_params["PedParams"],init_params["PedFitRange"],
                        fit_tail = FIT_TAIL, exp_fit_range = exp_fit_range)
                if pedopt is None:
                    print("PEDESTAL FIT FULLY FAILED... LIKELY A BUNK CHANNEL.  SKIPPING")
                    PedFitComplete = True
                    GoodPedFit = False
                    FitComplete = True
                    GoodFit = False
                    continue
                pl.PlotPedestal(pedxdata,pedydata,fu.gauss1,pedxdata,pedopt,"GaussPlusExpo")
                above_ped = 0
                past_ped = np.where(pedxdata > (pedopt[1] + 3*pedopt[2]))[0]
                if FIT_TAIL:
                    plt.plot(pedxdata[past_ped],pedydata[past_ped])
                    plt.plot(pedxdata[past_ped],fu.expo(pedxdata[past_ped],pedopt[3],
                                       pedopt[4],pedopt[5]))
                    above_ped = np.sum(pedydata[past_ped] - fu.expo(pedxdata[past_ped],pedopt[3],
                                       pedopt[4],pedopt[5]))
                else:
                    above_ped = np.sum(pedydata[past_ped] - fu.gauss1(pedxdata[past_ped],pedopt[0],
                                      pedopt[1],pedopt[2]))
                plt.show()
                print("4SIGMA PAST PED, EXP. SUBTRACTED: " + str(above_ped))
                if (above_ped < 300):
                    print("Low statistics beyond pedestal!  May just be fitting on fluctuations.")
                    skip_fit = str(raw_input("Skip this fit?"))
                    if skip_fit in ["y","Y","yes","Yes","YES"]:
                        PedFitComplete = True
                        GoodPedFit = False
                        FitComplete = True
                        GoodFit = False
                        continue

                ped_good = str(raw_input("Happy with pedestal fit? [y/N]:"))
                if ped_good in ["y","Y","yes","Yes","YES"]:
                    PedFitComplete = True
                    GoodPedFit = True
                else:
                    fit_min = str(raw_input("Exponential window min: "))
                    fit_max = str(raw_input("Exponential window max: "))
                    exp_fit_range = [float(fit_min),float(fit_max)]

            init_mean = np.argmax(above_ped)
            GainFinder.setInitMean(init_mean)
            UseDefault = "y"
            while not FitComplete:
                if UseDefault in ["y","Y","yes","Yes","YES"]:
                    popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist,
                            exclude_ped = True,subtract_ped = True)
                elif UseDefault in ["n","N","No","no","NO"]:
                    InitialParams = pin.GetInitialParameters(fittype)
                    popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist)
                if popt is None:
                    print("FIT FAILED.  WE'RE MOVING ON TO THE NEXT CHANNEL")
                    continue
                print("BEST FIT PARAMS: " + str(popt))
                #pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt,fittype)
                #print("Presenting combined final fit")
                #pl.PlotHistPEDAndPEs(xdata,ydata,pedopt,popt,fittype)
                pl.PlotHistPEDAndPEs_V2(xdata,ydata,pedopt,popt,fittype)
                if popt is None:
                    retry_fit = str(raw_input("Fit failed! Retry? [y/N]: "))
                    if retry_fit not in ["y","Y","yes","Yes","YES"]:
                        FitComplete = True
                        continue
                    else:
                        UseDefault = str(raw_input("Use default fit parameters? [y/N]"))
                approve_fit = str(raw_input("Fit converged! Happy with this fit? [y/N]: "))
                if approve_fit in ["y","Y","yes","Yes","YES"]:
                    FitComplete = True
                    GoodFit = True
                else:
                    retry = str(raw_input("Try again? [y/N]: "))
                    if retry not in ["y","Y","yes","Yes","YES"]:
                        FitComplete = True

            #Since we've made it out, save to the DB
            if GoodFit:
                db[fittype]["Channel"].append(channel_num)
                db[fittype]["RunNumber"].append(ap.RUNNUM)
                db[fittype]["LEDsOn"].append(ap.LED)
                db[fittype]["LEDPINs"].append(ap.PIN)
                db[fittype]["Date"].append(ap.DATE)
                db[fittype]["V"].append(ap.VOLTS)
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
                if fittype in ["SPE2Peaks"]:
                    db[fittype]["c1Height"].append(popt[0])
                    db[fittype]["c1Mu"].append(popt[1])
                    db[fittype]["c1Sigma"].append(popt[2])
                    db[fittype]["c2HScale"].append(popt[3])
                    db[fittype]["c2MScale"].append(popt[4])
                    db[fittype]["c2SScale"].append(popt[5])
                    db[fittype]["SCScale"].append(popt[6])
                    db[fittype]["c1Height_unc"].append(errs[0])
                    db[fittype]["c1Mu_unc"].append(errs[1])
                    db[fittype]["c1Sigma_unc"].append(errs[2])
                    db[fittype]["c2HScale_unc"].append(errs[3])
                    db[fittype]["c2MScale_unc"].append(errs[4])
                    db[fittype]["c2SScale_unc"].append(errs[5])
                    db[fittype]["SCScale_unc"].append(errs[6])
        with open(ap.DB,"w") as dbfile:
            json.dump(db,dbfile,sort_keys=False, indent=4)

    if ap.FIT == "DEAP":
        print("TRYING DEAP FIT")
