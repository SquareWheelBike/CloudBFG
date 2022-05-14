import numpy as np
import matplotlib.pyplot as plt
    
def CurrentSIM(Iprofile = None,I1 = None,I2 = None,delta = None,T = None,D = None): 
    if 'staircase' == Iprofile:
        delta = 5
        Nsp = iter
        Ns = 5
        Nb = 4
        Imag = np.array([- 40,- 80,- 120,- 160])
        T = np.arange(0,delta * Nsp * Ns * Nb - 1+delta,delta)
        #         T        = T*10^-3;
        T = np.transpose(T)
        I = np.zeros((Nsp * Ns * Nb,1))
        l = 1
        for k in np.arange(1,Nb * Nsp+1).reshape(-1):
            I[np.arange[[k - 1] * Ns + 1,k * Ns+1]] = Imag[l-1] * np.ones((Ns,1))
            l = l + 1
            if (l == Nb + 1):
                l = 1
        I = I * 10 ** - 3
    else:
        if 'deepdischarge' == Iprofile:
            delta = 5
            Ns = 10
            Nb = 2
            Imag = np.array([0,- 1000])
            T = np.arange(0,delta * Ns * Nb - 1+delta,delta)
            T = T * 10 ** - 3
            T = np.transpose(T)
            l = 1
            for k in np.arange(1,Nb+1).reshape(-1):
                I[np.arange[[k - 1] * Ns + 1,k * Ns+1]] = Imag[l-1] * np.ones((Ns,1))
                l = l + 1
                if (l == Nb + 1):
                    l = 1
            I = I * 10 ** - 3
        else:
            if 'rectangular' == Iprofile:
                #         delt = delta;
#         pulsewidth = T;
#         pulsetotal = D;
                delta = 1000
                Ns = 500
                Nb = 2
                Imag = np.array([- 1000,0])
                T = np.arange(0,delta * Ns * Nb - 1+delta,delta)
                T = T * 10 ** - 3
                T = np.transpose(T)
                l = 1
                for k in np.arange(1,Nb+1).reshape(-1):
                    I[np.arange[[k - 1] * Ns + 1,k * Ns+1]] = Imag[l-1] * np.ones((Ns,1))
                    l = l + 1
                    if (l == Nb + 1):
                        l = 1
                I = I * 10 ** - 3
                I = np.transpose(I)
            else:
                if 'rectangularnew' == Iprofile:
                    #         delta =  Sampling delta time in seconds
#         T = Pulse-Width in seconds
#         D = Total time in seconds
#         Id = current value
                    Ns_pulse = T / delta
                    Np = int(np.floor(D / T))
                    Nsp2 = int(Ns_pulse / 2)
                    Nb = 2
                    Nt = int(D / delta)
                    Imag = np.array([I1,I2])
                    T = np.arange(0,D+delta,delta)
                    T = np.transpose(T[1:])
                    l = 1
                    I = Imag[0] * np.ones((T.size,1))
                    for k in np.arange(1,Nb * Np+1).reshape(-1):
                        I[(np.arange((k - 1) * Nsp2 + 1,k * Nsp2+1))-1] = Imag[l-1] * np.ones((Nsp2,1), float)
                        l = l + 1
                        if (l == Nb + 1):
                            l = 1
                    if (Np * Ns_pulse != Nt):
                        Q = Nt - Np * Ns_pulse
                        I[np.arange[k * Nsp2 + 1,k * Nsp2 + Q+1]] = I(np.arange(1,Q+1))
                    I = I * 10 ** - 3
                else:
                    if 'UDDS' == Iprofile:
                        pass
                    else:
                        if 'simulated dynamic' == Iprofile:
                            pass
    
    # if len(varargin) == 0:
    #     close_('all')
    #     figure
    #     hold('on')
    #     grid('on')
    #     plt.plot(1000 * T,I,'-*')
    #     plt.xlabel('Time(ms)')
    #     plt.ylabel('Current (A)')
    #     set(gca,'fontsize',14)
    
    # return T,I
    
    return T,I
