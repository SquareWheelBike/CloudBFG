# 2021 by the University of Windsor.
import numpy as np
    
def battSIM(I = None,T = None,Batt = None,sigma_i = None,sigma_v = None,delta = None): 
    #     delta=0.1; # this should be constant in the input
    
    Kbatt = Batt.Kbatt
    Cbatt = Batt.Cbatt
    R0 = Batt.R0
    R1 = Batt.R1
    C1 = Batt.C1
    R2 = Batt.R2
    C2 = Batt.C2
    ModelID = Batt.ModelID
    alpha1 = np.exp(- (delta / (R1 * C1)))
    alpha2 = np.exp(- (delta / (R2 * C2)))
    h = 0
    soc = np.zeros((len(I),1))
    l = len(soc)
    soc[1] = 0.5
    # changed to 
    for k in np.arange(1,len(I)).reshape(-1):
        soc[k] = soc[k - 1] + (1 / (3600 * Cbatt)) * (I[k]) * (T[k] - T[k - 1])
        if soc[k] < 0:
            raise Exception('Battery is Empty!!')
        else:
            if soc[k] > 1:
                raise Exception('Battery is Full!!')
    
    ##
# Determination of OCV
    Vo = np.zeros((len(soc),1))
    zsoc = scaling_fwd(soc,0,1,0.175)
    for k in np.arange(1,len(zsoc)+1).reshape(-1):
        Vo[k] = Kbatt(1) + (Kbatt(2) / zsoc(k)) + (Kbatt(3) / (zsoc(k)) ** 2) + (Kbatt(4) / (zsoc(k)) ** 3) + (Kbatt(5) / (zsoc(k)) ** 4) + Kbatt(6) * zsoc(k) + Kbatt(7) * np.log(zsoc(k)) + Kbatt(8) * np.log(1 - zsoc(k))
    
    ##
#Determining current through R1 and R2
    
    x1 = np.zeros((len(I),1))
    x2 = np.zeros((len(I),1))
    for k in np.arange(1,len(I)+1).reshape(-1):
        x1[k + 1] = alpha1 * x1(k) + (1 - alpha1) * I(k)
        x2[k + 1] = alpha2 * x2(k) + (1 - alpha2) * I(k)
    
    I1 = np.zeros((len(I),1))
    I2 = np.zeros((len(I),1))
    for k in np.arange(1,len(I)+1).reshape(-1):
        I1[k] = x1(k + 1)
        I2[k] = x2(k + 1)
    
    ##
# Determination of Voltage drop and the Battery Terminal Voltage
    
    V = np.zeros((len(I),1))
    if 1 == ModelID:
        V = I * R0
    else:
        if 2 == ModelID:
            V = I * R0 + Vo + h
        else:
            if 3 == ModelID:
                V = I * R0 + I1 * R1 + Vo + h
            else:
                if 4 == ModelID:
                    V = I * R0 + I1 * R1 + I2 * R2 + Vo + h
    
    V = V + sigma_v * np.random.randn(Vo.shape)
    
    I = I + sigma_i * np.random.randn(I.shape)
    
    return V,I,soc,Vo
    
    
def scaling_fwd(x = None,x_min = None,x_max = None,E = None): 
    z = (1 - 2 * E) * (x - x_min) / (x_max - x_min) + E
    return z
    
    
def scaling_rev(z = None,x_min = None,x_max = None,E = None): 
    x = (z - E) * (x_max - x_min) / (1 - 2 * E) + x_min
    return x
    
    return V,I,soc,Vo