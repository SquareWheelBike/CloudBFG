# Client Pi

The clients (for now) are going to be on a Raspberry Pi, simulating a battery pack, with characterization data.

This is taking place of whichever embedded device will actually work in the final version.

Seeing as we should only really need Voltage and Current to perform SoC estimation, we can get away with using a single INA260 for both, since it has libraries for both Arduino and Python.
