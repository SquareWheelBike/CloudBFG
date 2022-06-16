from BattSim.BattSim import BattSim as bs
import BattSim.CurrentSIM as cs
import csv

# import ../res/K_para.csv into a list of dictionary values
with open('../res/K_para.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    K_para = list(reader)
print(K_para)