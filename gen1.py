# ## First Generation Estimation

# - [x] start by generating the curves for each of the sample k parameters using zsoc.py
# - [ ] Generate a full discharge curve (no noise) for a battery with matching k parameters to the sample curves
# - [ ] for each of the sample curves, and the sample curve, determine the rate of change throughout the curve
# - [ ] the best guess for which curve is the best fit is the one with the closest rate of change to the sample curve

# - The first guess can be using Vo from the simulator, for a perfect-match test case
# - The second run can be using Vout, the saggy loaded discharge curve

import src.zsoc as zsoc
import matplotlib.pyplot as plt
from src.BattSim.BattSim import BattSim
from src.BattSim.CurrentSIM import CurrentSIM
import numpy as np

# generate the curves for each of the sample k parameters using zsoc.py
batteries = zsoc.generate_curves(INPUTFILE, verbose=False, generate_csv=False, resolution=200)

# pick a random battery and create a battery object for it
# Kbatt: list, Cbatt: float, R0: float, R1: float, C1: float, R2: float, C2: float, ModelID:int, soc:float=0.5
target_battery = batteries[np.random.randint(0, len(batteries))]
sim_battery = BattSim(
    Kbatt=target_battery['Kbatt'],
    Cbatt = 1.9,
    R0 = 0.2,
    R1 = 0.1,
    C1 = 5,
    R2 = 0.3,
    C2 = 500,
    soc=1.0
) # note that only the Kbatt and soc is used for the simulation, the rest of the parameters are dummy values