import numpy as np
import scipy as sp
import scipy.optimize as scp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import json

DATADIR = "./DB/Final/"

def expo(x,A,l,C):
    return A*np.exp(x/l) + C

def ChargeToV(Q,A,l,C):
    return l*np.log((Q-C)/A)

if __name__=='__main__':
    gain_files = glob.glob(DATADIR+"*.json")
    df = None
    for f in gain_files:
        dat = None
        with open(f,"r") as f:
            dat = json.load(f)
            if df is None:
                df = pd.DataFrame(dat["EXP2SPE"])
            else:
                df = pd.concat([df,pd.DataFrame(dat["EXP2SPE"])],axis=0)
    print(df)
    TUBES = np.array(list(set(df["Channel"])))
    TUBES = np.arange(332,460,1)
    results = {"Channel":[], "Setpoint":[]}
    failures = {"Channel":[]}
    for cnum in TUBES:
        if cnum not in list(df["Channel"]):
            print("DID NOT FIND ANY DATA FOR CHANNELNUM %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        fig,ax = plt.subplots()
        myx = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "V"]
        myy = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "c1Mu"]*(6.2415E9)
        myyerr = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "c1Mu_unc"]*(6.2415E9)
        if (len(myx)<3):
            print("Not enough data to fit an exponential.")
            print("SKIPPING CHANNEL %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        ax.errorbar(myx,myy,yerr=myyerr,alpha=0.8,label="%i Data"%cnum,linestyle='None',marker='o',markersize=6)
        #ax.bar(y = myy,x = range(len(myx)), yerr = myyerr,label = cnum)
        #ax.xticks(range(len(myx)),myx)
        init_params = [5E5,100,1000]
        print(myx)
        print(myy)
        try:
            popt, pcov = scp.curve_fit(expo, myx, myy,p0=init_params, sigma=myyerr, maxfev=12000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT FOR CHANNEL %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        ax.plot(np.sort(myx),expo(np.sort(myx),popt[0],popt[1],popt[2]),label='Exponential Fit')
        print("1E7 GAIN VOLTAGE: %s"%(str(ChargeToV(1E7,popt[0],popt[1],popt[2]))))
        results["Channel"].append(cnum)
        results["Setpoint"].append(ChargeToV(1E7,popt[0],popt[1],popt[2]))
        leg = ax.legend(loc=1,fontsize=15)
        leg.set_frame_on(True)
        leg.draw_frame(True)
        ax.set_xlabel("Voltage") 
        ax.set_ylabel("SPE Charge Fit") 
        plt.xticks(rotation='30',fontsize=10)
        plt.title(("Best fit to SPE distribution"))
        plt.show()
    g = sns.FacetGrid(df,col='Channel',col_wrap=2,ylim=(0,0.002))
    g.map(sns.pointplot,"V","c1Mu",color=".3",ci=None)
    plt.savefig("GainPlots.pdf")
    print(results)
    print(failures)
