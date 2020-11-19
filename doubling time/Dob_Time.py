import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math

df = pd.read_csv("COVID_Dataset.csv")
pop = pd.read_csv("Population.csv")

#print(df.columns)

new_inf = [0 for i in range(250)]
new_mort = [0 for i in range(250)]

sz = len(df['Age'])
for i in range(sz):
    new_inf[df['Time of Infection'][i]] += 1
    if df['Outcome'][i] == 'Dead':
        new_mort[df['Time of reporting'][i]] += 1

tot_inf = new_inf[0:250]
tot_mort = new_mort[0:250]

for i in range(len(new_inf)-1):
    tot_inf[i+1] = tot_inf[i] + new_inf[i+1]

for i in range(1, 50):
    print(i, tot_inf[i], math.log(2)/math.log(tot_inf[i+1]/tot_inf[i]))



