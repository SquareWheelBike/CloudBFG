from src.tools import *
import src.zsoc as zsoc
import matplotlib.pyplot as plt
from src.BattSim.BattSim import BattSim
import src.BattSim.CurrentSIM as CurrentSIM
import numpy as np
from src.metrics import *


def find_curve(V: np.ndarray, batteries: list[dict]) -> dict:
    """
    find the curve that fits closest to the Vo of one of the batteries
    V: numpy array, volts
    batteries: list of dictionaries, battery cache from zsoc.py

    returns the dict battery cache object of the battery that matches the data
    """

    # this will NOT WORK if the datapoints being used are not numpy arrays
    assert (type(V) is np.ndarray)
    assert (all(type(battery['Vo']) is np.ndarray for battery in batteries))

    # find the closest match to the sample curve

    # diff contains tuple (V,) curve differences between the sample to each target curve for each sample battery
    diff = np.array([
        (
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

    # A*x0 + n*x1 = b
    # I*R0 + 1*Vo = Vbatt
    # V should contain Vbatt, I should contain Ibatt. We can use these to estimate R0 using least squares

    # for A, column 1 is I and column 2 is 1's
    A = np.array([I, np.ones(len(I))]).transpose()
    # for b, only one column is V
    b = V

    # solve the system of linear equations using least squares
    R0, Vo = np.linalg.lstsq(A, b, rcond=None)[0]

    return R0


def estimate_soc(V: float,  k: iter, I: float = 0, R0: float = 0) -> float:
    """
    estimate the soc of a battery at a given instantenous voltage and current

    V: float, volts
    I: float, amps
    k: list of floats, k-parameters of the battery
    R0: float, optional, ohms, offset to remove voltage sag from the battery discharge curve

    returns the soc of the battery at the given instantenous voltage and current using bisection root finding
    """

    # first generation of this will just generate the entire curve and do a lookup

    # start by compensating for the voltage sag, if given
    V = V - I * R0

    k = np.array(k)

    # each iteration is a resolution of 2 ** n
    ITERATIONS = 10

    def Vo(_soc: float) -> float:
        # _soc = (1 - 2 * 0.175) * _soc / 1 + 0.175
        return np.sum(
            np.array([1, 1 / _soc, 1 / _soc ** 2, 1 / _soc ** 3,
                     1 / _soc ** 4, _soc, np.log(_soc), np.log(1 - _soc)]) * k
        )

    # find the soc that matches the voltage
    upper = 1
    lower = 0
    soc = (upper + lower) / 2
    for i in range(ITERATIONS):
        # print(f'{i} {soc} {Vo(soc)}')
        if Vo(soc) > V:
            upper = soc
        else:
            lower = soc
        soc = (upper + lower) / 2

    return soc


if __name__ == '__main__':

    # test a bunch of times
    TESTS = 400
    RESOLUTION = 400
    delta = 3600 / RESOLUTION  # 1 hour, split into RESOLUTION points
    GRAPHS = True

    sigma_i = 0
    sigma_v = 0

    # generate the curves for each of the sample k parameters using zsoc.py
    INPUTFILE = 'res/K_para.csv'
    batteries = zsoc.generate_curves(
        INPUTFILE, verbose=False, generate_csv=False, resolution=RESOLUTION)
    for battery in batteries:
        battery['dV'] = derivative(battery['Vo'], delta)
        battery['dV2'] = derivative(battery['dV'], delta)

    k_error = []  # list of bools of whether a guess was correct
    r0_error = []  # list of R0 errors
    soc_error = []  # list of soc errors
    from progress.bar import Bar
    bar = Bar('Testing', max=TESTS)
    for i in range(TESTS):
        # pick a random battery and create a battery object for it
        target_battery = batteries[np.random.randint(0, len(batteries))]

        # run the chosen sample battery through the BattSim simulator to introduce noise
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
        # let I be a sine wave, offset for non constant discharge
        cycles = 5
        I = np.sin(np.linspace(0, 2*np.pi*cycles, RESOLUTION)) * Cbatt - Cbatt
        T = np.arange(0, delta * RESOLUTION, delta)
        Vbatt, Ibatt, soc, Vo = sim_battery.simulate(
            I, T, sigma_i=sigma_i, sigma_v=sigma_v)

        # add sag and noise to OCV curve
        V = Vo + Vbatt
        # reverse V so slope is positive, assuming input V vector is a discharge curve
        V = V[::-1]
        I = Ibatt[::-1]

        r0 = estimate_R0(V, I)
        r0_error.append(
            percent_error(np.array([r0]), np.array([target_battery['R0']]))
        )

        # apply the I*R0 load offset to the loaded curve
        Vnoisy = V
        V = V - r0 * I

        # find the closest match to the sample curve
        guess_batt = find_curve(V, batteries)

        k_error.append(percent_error(guess_batt['Vo'], target_battery['Vo']))

        # estimate the soc of the battery at the given instantenous voltage and current
        soc_est = []
        for _Vo, _soc in zip(target_battery['Vo'], target_battery['zsoc']):
            est = estimate_soc(V=_Vo, k=target_battery['k'])
            soc_est.append(est)
            soc_error.append(abs(est - _soc))

        # # plot the expected and actual curves for comparison (first one only)
        if (i == 0 and GRAPHS):
            fig, ax = plt.subplots(3, 1, sharex=True)
            ax[0].plot(Vnoisy, label='noisy loaded sample curve')
            ax[0].plot(target_battery['Vo'], label='correct OCV curve')
            ax[0].plot(V, label='load compensated curve')
            ax[0].plot(guess_batt['Vo'], label='estimated OCV curve')
            ax[0].legend()
            ax[0].set_title('Voltage Curves')
            ax[1].plot(Ibatt, label='noisy loaded sample curve')
            ax[1].set_title('Current Load')
            ax[2].plot(soc_est, label='estimated soc')
            ax[2].plot(target_battery['zsoc'], label='correct soc')
            ax[2].legend()
            ax[2].set_title('SOC')
            plt.show()

        bar.next()

    bar.finish()

    print(f'K error : {round(sum(k_error)/len(k_error)*100, 2)}%')
    print(f'R0 error : {round(sum(r0_error)/len(r0_error)*100, 2)}%')
    print(f'SOC error : {round(sum(soc_error)/len(soc_error)*100, 2)}%')
