# Client Pi

The clients (for now) are going to be on a Raspberry Pi, simulating a battery pack, with characterization data.

This is taking place of whichever embedded device will actually work in the final version.

Seeing as we should only really need Voltage and Current to perform SoC estimation, we can get away with using a single INA260 for both, since it has libraries for both Arduino and Python.

## Simulation Engine

Bala Bala has a simulation model for batteries with proper characteristics, written in Matlab. Rather than converting over to python, I should be able to run the matlab code using a Python script. I can redirect the `stdin` and `stdout` to `StringIO` objects in python, since matlab is an interpreted language.

A guide on where to start can be found [here](https://www.mathworks.com/help/matlab/matlab_external/redirect-standard-output-and-error-to-python.html).
