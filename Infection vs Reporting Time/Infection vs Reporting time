import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
df = pd.read_csv("COVID_Dataset.csv")
pop = pd.read_csv("Population.csv")

#print(df.columns)

new_inf = [0 for i in range(250)]
new_mort = [0 for i in range(250)]
sumtim = [0 for i in range(250)]
avgtim = [0 for i in range(250)]

sz = len(df['Age'])
for i in range(sz):
    new_inf[df['Time of Infection'][i]] += 1
    sumtim[df['Time of Infection'][i]] += df['Time of reporting'][i] - df['Time of Infection'][i]
    if df['Outcome'][i] == 'Dead':
        new_mort[df['Time of reporting'][i]] += 1

for i in range(250):
    if new_inf[i] == 0:
        continue
    avgtim[i] = sumtim[i]/new_inf[i]
tot_inf = new_inf[0:250]
tot_mort = new_mort[0:250]

for i in range(len(new_inf)-1):
    tot_inf[i+1] = tot_inf[i] + new_inf[i+1]
    tot_mort[i+1] = tot_mort[i] + new_mort[i+1]

plt.plot(range(200), avgtim[0:200], 'b-', label = "Time to report")
plt.legend()
plt.yscale('linear')
plt.axis([1,200,1,7])
plt.ylabel('Number of days')
plt.xlabel('Day number')
plt.show()

