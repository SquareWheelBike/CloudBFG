# Curve Fitting

Acceptable accuracy is 90% or more

## First Generation Estimation

- [x] start by generating the curves for each of the sample k parameters using zsoc.py
- [ ] Generate a full discharge curve (no noise) for a battery with matching k parameters to the sample curves
- [ ] for each of the sample curves, and the sample curve, determine the rate of change throughout the curve
- [ ] the best guess for which curve is the best fit is the one with the closest rate of change to the sample curve

- The first guess can be using Vo from the simulator, for a perfect-match test case
- The second run can be using Vout, the saggy loaded discharge curve

## Second Generation Estimation

- Second generation fitting will be done with noisy Vout curves
- This means that curve fitting will happen on the samples first, and then the clean curves will be compared to the sample set

## Third Generation Estimation

- Third generation will be where we start changing current throughout the discharge, since it will be rare that we will have a full, constant discharge curve.
- This means that outputs will have both sag noise, and voltage noise.

## Fourth Generation Estimation

- Incomplete curves will hopefully be able to be used, since it will be rare that a full discharge curve will be available.
- This is a lesser priority, since it is reasonable to request a full curve, although it will be difficult to collect from general use statistics.
