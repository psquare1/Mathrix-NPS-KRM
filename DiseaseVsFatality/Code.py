import pandas as pd
import matplotlib as plt

covid_df = pd.read_csv('COVID_Dataset.csv')

covid_df['DCat'] = ''

for i in range(len(covid_df['DCat'])):
    if covid_df['Diabetes'][i] == True and covid_df['Respiratory Illnesses'][i] == True and covid_df['Abnormal Blood Pressure'][i] == True:
        covid_df.at[i,'DCat'] = 'All 3 diseases'
    if covid_df['Diabetes'][i] == False and covid_df['Respiratory Illnesses'][i] == False and covid_df['Abnormal Blood Pressure'][i] == False:
        covid_df.at[i,'DCat'] = 'No other Condition'
    if covid_df['Diabetes'][i] == True and covid_df['Respiratory Illnesses'][i] == False and covid_df['Abnormal Blood Pressure'][i] == False:
        covid_df.at[i,'DCat'] = 'Only Diabetes'
    if covid_df['Diabetes'][i] == True and covid_df['Respiratory Illnesses'][i] == True and covid_df['Abnormal Blood Pressure'][i] == False:
        covid_df.at[i,'DCat'] = 'Diabetes & Respiratory'
    if covid_df['Diabetes'][i] == True and covid_df['Respiratory Illnesses'][i] == False and covid_df['Abnormal Blood Pressure'][i] == True:
        covid_df.at[i,'DCat'] = 'Diabetes & BP'
    if covid_df['Diabetes'][i] == False and covid_df['Respiratory Illnesses'][i] == True and covid_df['Abnormal Blood Pressure'][i] == True:
        covid_df.at[i,'DCat'] = 'Respiratory & BP'
    if covid_df['Diabetes'][i] == False and covid_df['Respiratory Illnesses'][i] == True and covid_df['Abnormal Blood Pressure'][i] == False:
        covid_df.at[i,'DCat'] = 'Only Respiratory'
    if covid_df['Diabetes'][i] == False and covid_df['Respiratory Illnesses'][i] == False and covid_df['Abnormal Blood Pressure'][i] == True:
        covid_df.at[i,'DCat'] = 'Only BP'

temp_df = pd.crosstab(covid_df['DCat'], covid_df['Outcome'])

temp2_df = temp_df.copy()
temp2_df = temp2_df.reset_index()
temp2_df['Alive%'] = 0.0
temp2_df['Dead%'] = 0.0
for i in range(8):
    x = temp2_df['Alive'][i]
    y = temp2_df['Alive'][i]+temp2_df['Dead'][i]
    temp2_df.at[i,'Alive%'] = float(str((x/y)*100)[:5])
    temp2_df.at[i,'Dead%'] = 100-temp2_df['Alive%'][i]
    
temp2_df.drop('Alive%', inplace = True, axis = 1)
temp2_df.drop('Dead', inplace = True, axis = 1)
temp2_df.drop('Alive', inplace = True, axis = 1)

print(temp2_df.plot(x = 'DCat',kind = 'bar',color = 'orange'))
