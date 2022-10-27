#!/usr/bin/python3

"""
We need to generate a dataset of plausible k-parameters, from the original set of 34 batteries.
"""

import numpy as np
import pandas as pd


# DONT USE, DOESNT WORK
def generate_k_parameters(cache: list, output: str = None, n: int = 1000) -> list:
    """
    Generate a dataset of plausible k-parameters, from the original set of 34 batteries. Keeps the original set, and just expands until we have n batteries.
    parameters:
        cache: a list of 34 batteries, each battery is a list of 8+ k-parameters
        output: the path to the output csv file
        n: the number of batteries to generate
    return:
        a list of n batteries, each battery is a list of 8+ k-parameters
    """

    # copy the original set
    batteries = np.array(cache)

    # for each k-parameter, calculate the mean and standard deviation for the original set
    means = np.mean(batteries, axis=0)
    stds = np.std(batteries, axis=0)
    # print(len(means), len(stds))

    # generate the rest
    batteries = np.concatenate((batteries,
                                np.array([np.random.normal(means, stds, size=len(means))
                                 for _ in range(n - len(batteries))])))

    # save the dataset
    if output:
        df = pd.DataFrame(batteries, columns=[f'K{i}' for i in range(
            8)] + [f'R{i}' for i in range(len(batteries[0]) - 8)])
        df.to_csv(output, index=False, header=False)

    return batteries
