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

def integrate_subtract(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    integrate the difference of two vectors
    a: numpy array, volts
    b: numpy array, volts

    returns the integrated result
    """
    return np.sum(np.abs(a - b))