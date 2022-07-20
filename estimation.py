# ## First Generation Estimation

# - [x] start by generating the curves for each of the sample k parameters using zsoc.py
# - [x] Generate a full discharge curve (no noise) for a battery with matching k parameters to the sample curves
# - [x] for each of the sample curves, and the sample curve, determine the rate of change throughout the curve
# - [x] the best guess for which curve is the best fit is the one with the closest rate of change to the sample curve

# - The first guess can be using Vo from the simulator, for a perfect-match test case
# - The second run can be using Vout, the saggy loaded discharge curve

from src.tools import *
import src.zsoc as zsoc
import matplotlib.pyplot as plt
from src.BattSim.BattSim import BattSim
import src.BattSim.CurrentSIM as CurrentSIM
import numpy as np

# Now that we have the full discharge curve of the battery, we can try to match it to one of the sample curves


def find_curve(V: np.ndarray, batteries: list[dict]) -> dict:
    """
    find the curve that fits closest to the Vo of one of the batteries
    V: numpy array, volts
    batteries: list of dictionaries, battery cache from zsoc.py

    returns the Kbatt of the battery that matches the data
    """

    # this will NOT WORK if the datapoints being used are not numpy arrays
    assert(type(V) is np.ndarray)
    assert(all(type(battery['Vo']) is np.ndarray for battery in batteries))

    # find the rate of change of the Vo curve
    delta = 3600 / 200  # using 200 points on everything
    dV = derivative(V, delta)
    dV2 = derivative(dV, delta)

    # find the closest match to the sample curve

    # diff contains tuple (V, dV, dV2) curve differences between the sample to each target curve for each sample battery
    diff = np.array([
        (
            # np.sum(np.abs(V - battery['Vo'])), # gen 1
            # integrate_subtract(dV, battery['dV']), # gen 2.1
            # integrate_subtract(dV2, battery['dV2']), # gen 2.1
            # gen 2.2, account for noise, use first derivative
            how_straight(V - battery['Vo']),
        ) for battery in batteries
    ])

    # TODO: rework estimation to use a weighted combination of the difference metrics
    match = batteries[np.argmin(np.sum(diff, axis=1))]

    return match

# Estimating R0 allows us to remove voltage sag from a battery discharge curve,
# and then use this offset to smooth out the curve.
# This is useful for estimating the OCV curve for a loaded battery.
# note: this requires a CHANGING LOAD, constant I will not do ANYTHING


def estimate_R0(V: np.ndarray, I: np.ndarray) -> float:
    """
    estimate the R0 of the battery, assuming a linear voltage sag

    V: numpy array, volts
    I: numpy array, amps

    returns the R0 of the battery, in ohms
    """

    # Ax + n = b
    # I*R0 + 1*Vo = Vbatt
    # I, Vbatt are known; solve for R0
    # x0 = I, x1 = 1

    # for a, column 1 is I and column 2 is 1's
    A = np.array([I, np.ones(len(I))]).T
    # for b, only one column is V
    b = V

    # solve the system of linear equations using least squares
    x = np.linalg.lstsq(A, b, rcond=None)[0]

    # R0 should be constant throughout the vector
    return x[0]

    # pass


if __name__ == '__main__':

    # test a bunch of times
    TESTS = 400
    RESOLUTION = 400
    delta = 3600 / RESOLUTION # 1 hour, split into RESOLUTION points

    sigma_i = 0
    sigma_v = 0

    # generate the curves for each of the sample k parameters using zsoc.py
    INPUTFILE = 'res/K_para.csv'
    batteries = zsoc.generate_curves(
        INPUTFILE, verbose=False, generate_csv=False, resolution=RESOLUTION)
    for battery in batteries:
        battery['dV'] = derivative(battery['Vo'], delta)
        battery['dV2'] = derivative(battery['dV'], delta)

    k_accuracy = []  # list of bools of whether a guess was correct
    r0_error = []  # list of R0 errors
    from progress.bar import Bar
    bar = Bar('Testing', max=TESTS)
    for i in range(TESTS):
        # pick a random battery and create a battery object for it
        target_battery = batteries[np.random.randint(0, len(batteries))]

        # run the chosen sample battery through the BattSim simulator to introduce noise
        # Kbatt: list, Cbatt: float, R0: float, R1: float, C1: float, R2: float, C2: float, ModelID:int, soc:float=0.5
        Cbatt = 2
        sim_battery = BattSim(
            Kbatt=target_battery['k'],
            Cbatt=Cbatt,
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
        # let I be a sine wave, offset for non constant discharge
        cycles = 5
        I = np.sin(np.linspace(0, 2*np.pi*cycles, RESOLUTION)) * Cbatt - Cbatt
        # I = np.ones(RESOLUTION) * sim_battery.Cbatt * -1
        T = np.arange(0, delta * RESOLUTION, delta)
        Vbatt, Ibatt, soc, Vo = sim_battery.simulate(
            I, T, sigma_i=sigma_i, sigma_v=sigma_v)

        # print('expected Kbatt:\t', target_battery['k'])

        # Vo + Vbatt = V with sag and noise
        V = Vo + Vbatt
        # reverse V so slope is positive, assuming input V vector is a discharge curve
        V = V[::-1]
        I = Ibatt[::-1]
        # dV = derivative(V, delta)
        # dV2 = derivative(dV, delta)

        guess_batt = find_curve(V, batteries)

        # # plot the expected and actual curves for comparison (first one only)
        if (i == 0):
            fig, ax = plt.subplots(2, 1, sharex=True)
            ax[0].plot(V, label='noisy loaded sample curve')
            ax[0].plot(target_battery['Vo'], label='correct OCV curve')
            ax[0].plot(Vo[::-1], label='guess OCV curve')
            ax[0].legend()
            ax[0].set_title('Voltage Curves')
            ax[1].plot(Ibatt, label='noisy loaded sample curve')
            ax[1].set_title('Current Load')
            plt.show()

        k_accuracy.append(all(a == b for a, b in zip(
            guess_batt['k'], target_battery['k'])))

        r0 = estimate_R0(V, I)

        if (i == 0):
            print('R0:\t', r0)
            print('R0 expected:\t', target_battery['R0'])
            print('R0 error:\t', r0 - target_battery['R0'])
        r0_error.append(
            np.abs(r0 - target_battery['R0']) / target_battery['R0']
        )
        bar.next()
    bar.finish()

    print(f'correctness : {sum(k_accuracy)/len(k_accuracy)*100}%')
    print(f'R0 error : {round(sum(r0_error)/len(r0_error)*100, 2)}%')
