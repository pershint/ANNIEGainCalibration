import numpy as np

gauss2= lambda x,p0: p0[0]*(1./np.sqrt(((p0[1]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
                                    p0[3]*(1./np.sqrt(((p0[4]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2)
gauss2InitialParams = [10000,0.00001,0.0001,100,0.0005,0.002]

gauss3= lambda x,p0: p0[0]*(1./np.sqrt(((p0[1]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
                                    p0[3]*(1./np.sqrt(((p0[4]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2) + \
                                    p0[6]*(1./np.sqrt(((p0[7]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[8])**2/p0[7]**2)

gauss3InitialParams = [10000,0.00001,0.0001,100,0.0005,0.002,10,0.003,0.003]

