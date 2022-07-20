# come up with meaningful metrics for the model's accuracy, for testing purposes.
# these will be used as reward functions later

import numpy as np
# from BattSim.BattSim import BattSim
from src.tools import *

# could also try comparing how close the zsoc curve chosen is to the noisy sample curve (perform curve_accuracy on the noisy curve and the guess k parameter curves

def percent_error(guess_vector:np.ndarray, correct_vector:np.ndarray) -> float:
    """
    calculate the percent error between two vectors

    guess_vector: list, vector of values to be compared
    correct_vector: list, vector of correct values

    returns: float, percent error, smaller is better
    """
    return integrate_subtract(guess_vector, correct_vector) / len(correct_vector)

# compare zsoc curves between two sets of k-parameters
# This is a better metric than just comparing raw soc curves since each coefficient will have a different range of possible values

def curve_accuracy_k(guess_k: list, target_k: list) -> float:
    """
    metric for how close the zsoc curves are between two sets of k-parameters
    guess_k: list, k parameters of the zsoc curve
    target_k: list, k parameters of the zsoc curve

    returns: float, percent error, smaller is better
    """

    return percent_error(soc_curve_k(guess_k, 200)[0], soc_curve_k(target_k, 200)[0])

