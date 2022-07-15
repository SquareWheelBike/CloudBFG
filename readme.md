# CloudBFG implelmentation

This is a cloud-based AI implementation of an SoC characterization algorithm.

Initial meeting notes can be found [here](notes.md).

## OCV Curves

The first version of the CloudBFG estimation algorithm will use a cache of pre-computed OCV curves.

For each of the batteries recorded in the [data](res/K_para.csv), the following OCV curve is generated, for use in estimating the K parameters of real batteries:

![OCV Curves](img/OCV_curves.png)

## Curve Fitting

Acceptable accuracy is 90% or more

### First Generation Estimation (completed)

- [x] start by generating the curves for each of the sample k parameters using zsoc.py
- [x] Generate a full discharge curve (no noise) for a battery with matching k parameters to the sample curves
- [x] look up the OCV curve for the battery with matching k parameters to the sample curves

- The guess can be using Vo from the simulator, for a perfect-match test case, as a proof of concept

#### Results

Since this is ideal-case, as soon as estimation was working, it was 100% accurate.

### Second Generation Estimation (ongoing)

- Second generation fitting will be done with noisy Vout curves
- This means that curve fitting will happen on the samples first, and then the clean curves will be compared to the sample set

#### First Attempt

- Taking the first and second derivatives of each OCV curve and comparing to the first and second derivatives of the sample is going to be the first attempt
- Going to account for voltage sag, but not noise

#### Results

- The results are not perfect, but it is correct about half the time and is close to the correct answer when it isn't correct

### Third Generation Estimation (untouched)

- Third generation will be where we start changing current throughout the discharge, since it will be rare that we will have a full, constant discharge curve.
- This means that outputs will have both sag noise, and voltage noise.

### Fourth Generation Estimation (untouched)

- Incomplete curves will hopefully be able to be used, since it will be rare that a full discharge curve will be available.
- This is a lesser priority, since it is reasonable to request a full curve, although it will be difficult to collect from general use statistics.
