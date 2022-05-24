from CurrentSIM import *
from battSIM import *

import numpy as np
import matplotlib.pyplot as plt
# close_('all')
# clear('all')
# dbstop('error')
k0 = - 9.082
k1 = 103.087
k2 = - 18.185
k3 = 2.062
k4 = - 0.102
k5 = - 76.604
k6 = 141.199
k7 = - 1.117
Kbatt = np.array([[k0], [k1], [k2], [k3], [k4], [k5], [k6], [k7]])
batt_model = 3

# Batt is implicitly declared in matlab, but we need to define it here
class Battery:
    def __init__(self):
        self.Kbatt = None
        self.Cbatt = None
        self.R0 = None
        self.R1 = None
        self.R2 = None
        self.C1 = None
        self.C2 = None
        self.ModelID = None
        self.alpha1 = None
        self.alpha2 = None
Batt = Battery()

Batt.Kbatt = Kbatt
Batt.Cbatt = 1.9
Batt.R0 = 0.2
Batt.R1 = 0.1
Batt.C1 = 5
Batt.R2 = 0.3
Batt.C2 = 500
Batt.ModelID = batt_model
# current simulation parameters
delta = 100 * 10 ** (- 3)
Tc = 10

D = 100

Id = - 500

Batt.alpha1 = np.exp(- (delta / (Batt.R1 * Batt.C1)))
Batt.alpha2 = np.exp(- (delta / (Batt.R2 * Batt.C2)))
# current simulation
T, I = CurrentSIM('rectangularnew', - Id, Id, delta, Tc, D)
# SNR and noise parameters
SNR = 50
sigma_i = 0

sigma_v = 10 ** (- SNR / 20)

# send current into the batery simulater
Vbatt, Ibatt, __, Vo = battSIM(I, T, Batt, sigma_i, sigma_v, delta)
# current plotting
hI = figure
hold('on')
grid('on')
box('on')
subplot(211)
box('on')
grid('on')
plt.plot(T, Ibatt, 'linewidth', 2)
plt.xlabel('Time (sec)')
plt.ylabel('Current (mA)')
grid('on')
subplot(212)
box('on')
grid('on')
plt.plot(T, Vbatt, 'linewidth', 2)
grid('on')
plt.xlabel('Time (sec)')
plt.ylabel('Voltage (V)')
