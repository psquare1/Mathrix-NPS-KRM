import pandas as pd

covid_df = pd.read_csv('COVID_Dataset.csv')

import math
covid_df['Age_Cat'] = ""
for i in range(len(covid_df['Age_Cat'])):
    x = int(covid_df['Age'][i])
    if x%10 == 0:
        t = str(x)+'-'+str(x+10)
    else:
        t = str(math.floor(x/10)*10)+'-'+str(math.ceil(x/10)*10)
    covid_df.at[i,'Age_Cat'] = t

covid_df['Avg Reporting Time'] = 0
for i in range(len(covid_df['Avg Reporting Time'])):
    covid_df.at[i,'Avg Reporting Time'] = covid_df['Time of reporting'][i] - covid_df['Time of Infection'][i]
    
temp2_df = covid_df.groupby('Age_Cat').mean()

ax = temp2_df.plot(y = 'Avg Reporting Time', kind = 'bar', color = 'orange', title = 'Age Vs Average Reporting')
print(ax)
