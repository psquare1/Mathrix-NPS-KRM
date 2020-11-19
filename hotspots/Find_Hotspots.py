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

day_num = 88

new_inf_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]

sz = len(df['Age'])

for i in range(sz):
    new_inf_area[df['Time of Infection'][i]][df['y location'][i]-1][df['x location'][i]-1] += 1 
    
tot_inf_area = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]
tot_inf_perc = [[[0 for i in range(20)] for j in range(20)] for k in range(250)]

for x in range(20):
    for y in range(20):
        tot_inf_area[0][y][x] = new_inf_area[0][y][x]

for i in range(249):
    for x in range(20):
        for y in range(20):
            tot_inf_area[i+1][y][x] = tot_inf_area[i][y][x]+new_inf_area[i+1][y][x]
            tot_inf_perc[i][y][x] = tot_inf_area[i][y][x]/pop['Population'][20*x+y]

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

for time in range(250):
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

    if time == day_num:
        for i in concom:
            print(i)
            

    hmapda = [[len(concom) for y in range(20)] for x in range(20)]
    for i in range(len(concom)):
        for j in concom[i]:
            hmapda[district[j][0]][district[j][1]] = len(concom)-i-1

    if time == day_num:
        im = plt.imshow(hmapda, cmap = "cubehelix", interpolation = "nearest")
        plt.title("Day" + str(day_num))
        plt.show()

                        
