# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
import scipy.optimize as sco
import scipy.stats as sts
import lib.Functions as fu

maxes = []
for i in range(10000):
    maxes.append(np.max(scp.randn(30)))
    
bin_height, bin_edges = np.histogram(maxes,bins=100)
bin_width = bin_edges[1]-bin_edges[0]
bin_edges_t = bin_edges[0:len(bin_edges) -1]
bin_centers = np.array(bin_edges_t) - (bin_width/2)
popt,pcov = sco.curve_fit(fu.gauss1,bin_centers,bin_height,p0=[1000,2,2])
yfit = fu.gauss1(bin_centers,popt[0],popt[1],popt[2])
plt.hist(maxes,bins=100)
plt.plot(bin_centers,yfit)
plt.show()
popt,pcov = sco.curve_fit(fu.Beta,bin_centers,bin_height,p0=[1000,0.1,0.1,10])
yfit = fu.gauss1(bin_centers,popt[0],popt[1],popt[2])
plt.hist(maxes,bins=100)
plt.plot(bin_centers,yfit)
plt.show()
