# come up with meaningful metrics for the model's accuracy, for testing purposes.
# these will be used as reward functions later

import numpy as np
from BattSim.BattSim import BattSim
from tools import *

# compare zsoc curves between two sets of k-parameters
# This is a better metric than just comparing raw soc curves since each coefficient will have a different range of possible values


def curve_accuracy(guess_k: list, target_k: dict) -> float:
    """
    metric for how close the zsoc curves are between two sets of k-parameters
    guess_k: list, k parameters of the zsoc curve
    target_k: dict, battery parameters of the sample curve
    """

    return integrate_subtract(soc_curve_k(guess_k, 200)[0], soc_curve_k(target_k, 200)[0])
