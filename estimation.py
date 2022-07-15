# ## First Generation Estimation

# - [x] start by generating the curves for each of the sample k parameters using zsoc.py
# - [x] Generate a full discharge curve (no noise) for a battery with matching k parameters to the sample curves
# - [x] for each of the sample curves, and the sample curve, determine the rate of change throughout the curve
# - [x] the best guess for which curve is the best fit is the one with the closest rate of change to the sample curve

# - The first guess can be using Vo from the simulator, for a perfect-match test case
# - The second run can be using Vout, the saggy loaded discharge curve

from src.tools import derivative
import src.zsoc as zsoc
import matplotlib.pyplot as plt
from src.BattSim.BattSim import BattSim
import src.BattSim.CurrentSIM as CurrentSIM
import numpy as np

# generate the curves for each of the sample k parameters using zsoc.py
INPUTFILE = 'res/K_para.csv'
batteries = zsoc.generate_curves(
    INPUTFILE, verbose=False, generate_csv=False, resolution=200)

# pick a random battery and create a battery object for it
target_battery = batteries[np.random.randint(0, len(batteries))]


# run the chosen sample battery through the BattSim simulator to introduce noise
# Kbatt: list, Cbatt: float, R0: float, R1: float, C1: float, R2: float, C2: float, ModelID:int, soc:float=0.5
sim_battery = BattSim(
    Kbatt=target_battery['k'],
    Cbatt=2,
    R0=target_battery['R0'],
    R1=0.1,
    C1=5,
    R2=0.3,
    C2=500,
    soc=1.0,
    ModelID=1,
)  # note that only the Kbatt and soc is used for the simulation, the rest of the parameters are dummy values

# simulate full discharge curve for the battery
# discharge at 1C for 1h
I = np.ones(200) * sim_battery.Cbatt * -1
T = np.arange(0, 3600, 3600/200)
Vbatt, Ibatt, soc, Vo = sim_battery.simulate(I, T, sigma_v=0)


# calculate first and second derivatives of all curves for use later
delta = 3600 / 200  # using 200 points on everything
for battery in batteries:
    battery['dV'] = derivative(battery['Vo'], delta)
    battery['dV2'] = derivative(battery['dV'], delta)


# Now that we have the full discharge curve of the battery, we can try to match it to one of the sample curves
def find_curve(V: np.ndarray, batteries: list[dict]):
    """
    find the curve that fits closest to the Vo of one of the batteries
    V: numpy array, volts
    batteries: list of dictionaries, battery cache from zsoc.py

    returns the Kbatt of the battery that matches the data
    """

    # reverse V so slope is positive,
    # assuming input V vector is a discharce curve
    V = V[::-1]

    # find the rate of change of the Vo curve
    delta = 3600 / 200  # using 200 points on everything
    dV = derivative(V, delta)
    dV2 = derivative(dV, delta)

    # this will NOT WORK if the datapoints being used are not numpy arrays
    assert(type(V) is np.ndarray)
    assert(all(type(battery['Vo']) is np.ndarray for battery in batteries))

    # find the closest match to the sample curve

    # diff contains tuple (V, dV, dV2) curve differences between the sample to each target curve for each sample battery
    diff = np.array([
        (
            np.sum(np.abs(V - battery['Vo'])),
            np.sum(np.abs(dV - battery['dV'])),
            np.sum(np.abs(dV2 - battery['dV2'])),
        ) for battery in batteries
    ])

    # TODO: rework estimation to use a weighted combination of the difference metrics
    match = batteries[np.argmin(diff[1])]

    return match


# shuffle batteries so that test can start with a random battery
batteries = batteries[:]
np.random.shuffle(batteries)

print('expected Kbatt:\t', target_battery['k'])

# Vo + Vbatt = Vout with voltage sag for a non noisy uniform load
print('actual Kbatt:\t', find_curve(Vo + Vbatt, batteries)['k'])
