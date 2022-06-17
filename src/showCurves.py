# A demo file to graph the OCV curves, overlayed on each other, for all batteries in the K_para.csv file.

import zsoc
import matplotlib.pyplot as plt

INPUTFILE = '../res/K_para.csv'
OUTPUTFOLDER = '../res/zsoc_curves'
DECIMALS = 4
batteries = zsoc.generate_curves(INPUTFILE, decimals=4, verbose=False, generate_csv=False, resolution=200)[1:]

for battery in batteries:
    plt.plot(battery[-2], battery[-1], label=battery[0])
plt.title(label='OCV curves for all batteries')
plt.xlabel(xlabel='zsoc')
plt.ylabel(ylabel='Vo')
plt.grid(True)
# plt.legend()
plt.show()
