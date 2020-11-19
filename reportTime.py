# to find the correlation between time taken to report and the survival percentage
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("COVID_Dataset.csv")
print(df.columns)
df["Time to report"] = df["Time of reporting"]-df["Time of Infection"]
total = []
alive = []

for i in range(1,8):
    total.append(len(df.loc[df["Time to report"]==i]))
    alive.append(len(df.loc[(df["Time to report"]==i) & (df["Outcome"] == "Alive")]))

#tot = len(df.loc[df["Time to report"]==1])
#ali = len(df.loc[(df["Time to report"]==1) & (df["Outcome"] == "Alive")])
y_ax = []

for i in range(7):
    #print(i)
    #print(total[i])
    #print(alive[i])
    #print("{0:.2f}".format(alive[i]/total[i]*100))
    y_ax.append(float("{0:.2f}".format(alive[i]/total[i]*100)))
    #print()

print(y_ax)
fig = plt.figure()
x_ax = ['1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days']
axes = fig.add_axes([0.07,0.07,0.7,0.7])
axes.set_title("Survival with respect to reporting time")
axes.set_xlabel("Days to report")
axes.set_ylabel("Survival percentage")
plt.ylim(97, 98)
axes.bar(x_ax, y_ax)
plt.show()
