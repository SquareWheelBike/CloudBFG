# A demo file to graph the OCV curves, overlayed on each other, for all batteries in the K_para.csv file.

import src.zsoc as zsoc
import matplotlib.pyplot as plt

INPUTFILE = 'res/K_para.csv'
DECIMALS = 4

# NOTE: the output from generate_curves uses basic datatypes, but has been designed to be able to drop into a pandas dataframe as-is
import time
batteries = zsoc.generate_curves(INPUTFILE, verbose=False, generate_csv=False, resolution=200)

for battery in batteries:
    plt.plot(battery['zsoc'], battery['Vo'], label=battery['sample'])
plt.title(label='OCV curves for all batteries')
plt.xlabel(xlabel='zsoc')
plt.ylabel(ylabel='Vo')
plt.grid(True)
# plt.legend()
plt.show()
