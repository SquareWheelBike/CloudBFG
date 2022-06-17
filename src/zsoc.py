"""
Use batteries in ../res/K_para.csv to generate a set of zsoc curves for each battery.
"""

import csv
import numpy as np
import os
from math import log


def generate_curves(inputfile: str, outputfolder: str=None, decimals: int=4, generate_csv: bool = True, verbose: bool = False, resolution: int = 100):

    INPUTFILE = inputfile
    OUTPUTFOLDER = outputfolder
    DECIMALS = decimals
    NPOINTS = resolution

    if OUTPUTFOLDER is None and generate_csv:
        raise ValueError('Must specify an output folder if generating a CSV file')

    # import ../res/K_para.csv into a list of dictionary values
    print('Importing all data for batteries:') if verbose else None
    with open(INPUTFILE, 'r') as csvfile:
        reader = csv.reader(csvfile)
        K_para = list(reader)

    # print all data
    if verbose:
        for n, entry in enumerate(K_para[1:]):
            for i, j in zip(K_para[0], entry):
                print(i, j)
            print('-' * 20)

    # if OUTPUTFOLDER does not exist, create it
    if generate_csv:
        if not os.path.exists(OUTPUTFOLDER):
            print(f'Creating {OUTPUTFOLDER}/') if verbose else None
            os.makedirs(OUTPUTFOLDER)
        else:
            print(f'Directory {OUTPUTFOLDER}/ already exists. Clearing contents.') if verbose else None
            for file in os.listdir(OUTPUTFOLDER):
                os.remove(f'{OUTPUTFOLDER}/{file}')

        print('Output folder setup complete.') if verbose else None

    def __scaling_fwd(x, x_min, x_max, E):
        return (1 - 2 * E) * (x - x_min) / (x_max - x_min) + E

    # determination of OCV (generate Vo
    l = NPOINTS
    zsoc = __scaling_fwd(np.linspace(0, 1, l), 0, 1, 0.175)
    K_para[0].append('zsoc')
    K_para[0].append('Vo')
    # print('zsoc:', zsoc)
    for entry in K_para[1:]:
        print('Generating zsoc curve for battery', entry[0], entry[1:]) if verbose else None
        Kbatt = list(map(float, entry[4:]))
        Vo = np.zeros(l)  # create Vo (OCV voltage vector)

        for k, zk in enumerate(zsoc):
            Vo[k] = Kbatt[0]\
                + Kbatt[1] / zk\
                + Kbatt[2] / zk ** 2\
                + Kbatt[3] / zk ** 3\
                + Kbatt[4] / zk ** 4\
                + Kbatt[5] * zk\
                + Kbatt[6] * log(zk)\
                + Kbatt[7] * log(1 - zk)

        entry.append(zsoc)
        entry.append(Vo)

        # store Vo in a csv file
        if generate_csv:
            filename = f'{OUTPUTFOLDER}/Vo_' + '_'.join(entry[:4]) + '.csv'
            print('storing Vo in', filename, end='...') if verbose else None
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['soc', 'Vo'])
                for v, zk in zip(Vo, zsoc):
                    writer.writerow([round(zk, DECIMALS), round(v, DECIMALS)])
            print(' Done.') if verbose else None
    
    return K_para


if __name__ == '__main__':
    INPUTFILE = '../res/K_para.csv'
    OUTPUTFOLDER = '../res/zsoc_curves'
    DECIMALS = 4
    NPOINTS = 200
    generate_curves(INPUTFILE, OUTPUTFOLDER, DECIMALS, verbose=True, resolution=NPOINTS)
