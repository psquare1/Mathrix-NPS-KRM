import pandas as pd
import matplotlib as plt
import seaborn as sns
import math

covid_df = pd.read_csv('COVID_Dataset.csv')

covid_df['Age_Cat'] = ""
for i in range(len(covid_df['Age_Cat'])):
    x = int(covid_df['Age'][i])
    if x%10 == 0:
        t = str(x)+'-'+str(x+10)
    else:
        t = str(math.floor(x/10)*10)+'-'+str(math.ceil(x/10)*10)
    covid_df.at[i,'Age_Cat'] = t
    
temp_df = pd.crosstab(covid_df.Age_Cat,covid_df.Outcome)

temp_df['Alive%'] = 0.0
for i in range(len(temp_df['Alive'])):
    m = str(i*10)+'-'+str((i*10)+10)
    x = temp_df['Alive'][i]+temp_df['Dead'][i]
    y = temp_df['Alive'][i]
    t = y/x
    temp_df.at[m,'Alive%'] = float(str(t*100)[:5])
temp_df['Dead%']=0.0
for i in range(len(temp_df['Alive'])):
    m = str(i*10)+'-'+str((i*10)+10)
    temp_df.at[m,'Dead%'] = 100-temp_df['Alive%'][i]
    
temp_df.drop('Dead', inplace=True, axis = 1)
temp_df.drop('Alive', inplace=True, axis = 1)
temp_df.drop('Alive%', inplace=True, axis = 1)

print(temp_df.plot(kind='bar',color = 'orange',title = 'Age Vs Fatality'))
