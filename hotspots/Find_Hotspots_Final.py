#Code that determines how many people are infected overall till a certain day

#Columns of Covid are 'Time of Infection', 'Time of reporting', 'x location', 'y location',
#       'Age', 'Diabetes', 'Respiratory Illnesses', 'Abnormal Blood Pressure',
#       'Outcome'

#Columns of pop are 'x location', 'y location', 'Population'

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("COVID_Dataset.csv")
pop = pd.read_csv("Population.csv")

day_num = 29
day_nums = [30, 60, 100, 150, 200]

new_inf = [0]*250
new_mort = [0]*250

sz = len(df['Age'])
for i in range(sz):
    new_inf[df['Time of Infection'][i]] += 1
    if df['Outcome'][i] == 'Dead':
        new_mort[df['Time of reporting'][i]] += 1

tot_inf = new_inf[0:250]
tot_mort = new_mort[0:250]

for i in range(len(new_inf)-1):
    tot_inf[i+1] = tot_inf[i] + new_inf[i+1]
    tot_mort[i+1] = tot_mort[i] + new_mort[i+1]

new_inf_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]
new_mort_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]

for i in range(sz):
    new_inf_area[df['Time of Infection'][i]][df['y location'][i]-1][df['x location'][i]-1] += 1
    if df['Outcome'][i] == 'Dead':
        new_mort_area[df['Time of reporting'][i]][df['y location'][i]-1][df['x location'][i]-1] += 1

    
tot_inf_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]
tot_inf_perc = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]
tot_mort_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]

for x in range(20):
    for y in range(20):
        tot_inf_area[0][y][x] = new_inf_area[0][y][x]
        tot_mort_area[0][y][x] = new_mort_area[0][y][x]

for i in range(249):
    for x in range(20):
        for y in range(20):
            tot_inf_area[i+1][y][x] = tot_inf_area[i][y][x]+new_inf_area[i+1][y][x]
            tot_inf_perc[i][y][x] = tot_inf_area[i][y][x]/pop['Population'][20*x+y]
            tot_mort_area[i+1][y][x] = tot_mort_area[i][y][x]+new_mort_area[i+1][y][x]

pop_den = [[0 for i in range(20)] for j in range(20)]
for y in range(20):
    for x in range(20):
        pop_den[y][x] = pop['Population'][20*x+y]


wdist = [0 for i in range(250)]
vdist = [0 for i in range(250)]
for time in range(250):
    for y in range(20):
        for x in range(20):
            wdist[time] = max(wdist[time], tot_inf_perc[time][y][x])
            vdist[time] = max(vdist[time], tot_inf_area[time][y][x])

neigh = [[ [] for i in range(20)] for j in range(20)]
for x in range(20):
    for y in range(20):
        if x < 19:
            neigh[y][x].append([y, x+1])
        if x > 0:
            neigh[y][x].append([y, x-1])
        if y < 19:
            neigh[y][x].append([y+1, x])
        if y > 0:
            neigh[y][x].append([y-1, x])

#debug prints
#print(neigh[2][3], neigh[0][19])

SW_spot = [[0 for i in range(250)] for j in range(3)]
centre_spot = [[0 for i in range(250)] for j in range(3)]
NE_spot = [[0 for i in range(250)] for j in range(3)]
others = [[0 for i in range(250)] for j in range(3)]


for time in range(249):
    cutoffw = wdist[time]/4
    cutoffv = vdist[time]/4
    district = []
    for x in range(20):
        for y in range(20):
            if tot_inf_perc[time][y][x] > cutoffw and tot_inf_area[time][y][x] > cutoffv:
                district.append([y,x])

    heft = len(district)
    adj = [ [] for i in range(heft)]
    for i in range(heft):
        for j in range(heft):
            if i == j:
                continue
            if (district[i][0] - district[j][0])*(district[i][0] - district[j][0]) + (district[i][1] - district[j][1])*(district[i][1] - district[j][1]) <= 4:
                adj[i].append(j)

    vis = [0 for i in range(heft)]
    connum = -1
    concom = []
    queue = []
    for i in range(heft):
        if vis[i] == 0:
            queue.append(i)
            connum += 1
            concom.append([i])
            vis[i] = 1
            while queue:
                cur = queue.pop(0)
                for j in adj[cur]:
                    if vis[j] == 0:
                        vis[j] = 1
                        queue.append(j)
                        concom[connum].append(j)

    for i in range(len(concom)-1,-1,-1):
        if len(concom[i]) < 4:
            concom.pop(i)

    fluff = []
    for i in range(len(concom)):
        fluff.append([])
        for j in range(len(concom[i])):
            if concom[i][j] not in fluff[i]:
                fluff[i].append([district[concom[i][j]][0], district[concom[i][j]][1]])

    for i in range(len(concom)):
        for j in range(len(concom[i])):
            for k in neigh[fluff[i][j][0]][fluff[i][j][1]]:
                if time == 29 and i == 0:
                    print(k, fluff[i])
                if k not in fluff[i]:
                    fluff[i].append(k)
        
    hmapda = [[len(concom) for y in range(20)] for x in range(20)]
    for i in range(len(concom)):
        for j in range(len(fluff[i])):
            hmapda[fluff[i][j][0]][fluff[i][j][1]] = len(concom)-i-1

    if time in day_nums:
        im = plt.imshow(hmapda, cmap = "cubehelix", interpolation = "nearest")
        plt.title("Day" + str(time))
        plt.show()

    connum = len(concom)
    sumy = [0 for i in range(connum)]
    cases = [0 for i in range(connum)]
    deaths = [0 for i in range(connum)]
    for i in range(connum):
        for j in range(len(fluff[i])):
            #sumy[i] += district[concom[i][j]][0]
            cases[i] += tot_inf_area[time][fluff[i][j][0]][fluff[i][j][1]]
            deaths[i] += tot_mort_area[time][fluff[i][j][0]][fluff[i][j][1]]

    if time > 20:
        SW_spot[0][time] = cases[0]
        centre_spot[0][time] = cases[1]
        NE_spot[0][time] = cases[2]
        SW_spot[1][time] = deaths[0]
        centre_spot[1][time] = deaths[1]
        NE_spot[1][time] = deaths[2]

for i in range(21, 249):
    others[0][i] = tot_inf[i] - SW_spot[0][i] - NE_spot[0][i] - centre_spot[0][i]
    others[1][i] = tot_mort[i] - SW_spot[1][i] - NE_spot[1][i] - centre_spot[1][i]
    
                       
#plt.plot(range(21,240), tot_inf[21:240], 'y-', label = "Total Infections")
plt.plot(range(21,240), SW_spot[1][21:240], 'm-', label = "SW Hotspot")
plt.plot(range(21,240), centre_spot[1][21:240], 'g-', label = "Center Hotspot")
plt.plot(range(21,240), NE_spot[1][21:240], 'k-', label = "NE hotspot")
plt.plot(range(21,240), others[1][21:240], 'r-', label = "other districts")
plt.legend()
plt.yscale('linear')   
plt.axis([21,240,1,7000])
plt.ylabel('Total deaths')
plt.xlabel('Day number')
plt.show()

                        
