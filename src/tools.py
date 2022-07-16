import numpy as np

def derivative(L: np.ndarray, dt: float = 1) -> np.ndarray:
    """
    find the rate of change of a vector
    L: numpy array, volts, dt: float, seconds between datapoints

    returns the rate of change of the vector
    """
    if len(L) < 2:
        return 0
    if type(L) is not np.ndarray:
        L = np.array(L)
    return (L[1:] - L[:-1]) / dt