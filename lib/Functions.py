import numpy as np

#def gauss2(x,p0):
#    return p0[0]*(1./(p0[1]*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
#                                    p0[3]*(1./(p0[4]*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2) 
#
#
#def gauss3(x,*p0):
#    return p0[0]*(1./np.sqrt(((p0[1]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
#                                    p0[3]*(1./np.sqrt(((p0[4]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2) + \
#                                    p0[6]*(1./np.sqrt(((p0[7]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[8])**2/p0[7]**2)
#


gauss1= lambda x,C1,m1,s1: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m1)**2)/s1**2)

gaussPlusExpo= lambda x,C,m,s,D,l,t: (D*(np.exp(-(x-t)*l))+C*(1*np.sqrt(2*np.pi))**np.exp(-(1./2.)*(x-m)**2/s**2))

gauss2= lambda x,C1,m1,s1,C2,m2,s2: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m1)**2)/s1**2) + \
                                    C2*(1./(s2*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m2)**2)/s2**2)

gauss2InitialParams = np.array([300,0.001,0.0001,100,0.002,0.0005])

gauss2dep= lambda x,C1,m,s,Cf,f1,f2: C1*(1./(s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m)**2)/s**2) + \
                                    C1*Cf*(1./(f2*s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-(f1*m))**2)/(f2*s)**2)

gauss2depInitialParams = np.array([300,0.001,0.0001,0.5,2,1.5])
gauss2depLB = [0, 0, 0, 0, 1.5, 1]
gauss2depUB = [1E3, 0.001, 0.001, 1, 2.5, 2]

gauss3= lambda x,C1,m1,s1,C2,m2,s2,C3,m3,s3: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m1)**2/s1**2) + \
                                    C2*(1./(s2*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m2)**2/s2**2) + \
                                    C3*(1./(s3*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m3)**2/s3**2)

gauss3InitialParams = np.array([10000,0.00001,0.0001,100,0.0005,0.002,10,0.003,0.003])
gauss3LB = [0, 0, 0, 0, 0.0001, 0, 0, 0, 0.0005]
gauss3UB = [1E6, 0.001, 0.0005, 1E4, 0.006, 0.01, 1E3, 0.01, 0.05]


gauss2InitialParams = np.array([10000,0.00001,0.00001,100,0.001,0.0005])

gauss4= lambda x,C1,m1,s1,C2,m2,s2,C3,m3,s3,C4,m4,s4: C1*(1./(s1*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m1)**2/s1**2) + \
                                    C2*(1./(s2*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m2)**2/s2**2) + \
                                    C3*(1./(s3*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m3)**2/s3**2) + \
                                    C4*(1./(s4*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m4)**2/s4**2)

gauss4InitialParams = np.array([1000,450,6,1000,578,6,1000,750,6,1000,867,5])

