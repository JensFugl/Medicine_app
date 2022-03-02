# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 13:50:31 2022

@author: jensr
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns

plt.close('all')

bd = pd.read_pickle("bd.pkl")

bd['Price_pr_mg'] = bd['Price']/bd['Aktivt_stof']

bd = bd[bd['Price_pr_mg']>0.002] 


'''
fig, ax = plt.subplots()
bd['Aktivt_stof'].hist()
bd['Styrke'].hist(bins = 500)


fig1, ax = plt.subplots()
sns.scatterplot(data=bd, x= 'Date', y='Price_pr_mg')


fig1, ax = plt.subplots()
sns.lineplot(data=bd, x= 'Date', y='Price_pr_mg', estimator = "min")

fig1, ax = plt.subplots()
sns.lineplot(data=bd['Price_pr_mg'])
'''



user = {"Medicine_left" : 0, "Daily_use" : 800, "Days_left": 0, "Money_spent" : 0, "Date" : 0 }

everyday = pd.date_range('2016-11-21', '2022-01-10', freq='D')
#lol = pd.date_range('2016-11-21', '2022-01-10', freq='14D')

a = pd.DataFrame(everyday, columns = ['Date'])
b = bd[bd['Price_pr_mg'].isin(bd.groupby('Date').min()['Price_pr_mg'])]
b = pd.concat([b, a]).sort_values(by= 'Date')
b = b.fillna(method='ffill')

def buyEvent(df, user, date):
    day = df[df['Date'] == date]

    buy = day[day['Price_pr_mg'].isin(day.groupby(day.Date).min()['Price_pr_mg'])]
    user['Medicine_left'] = user['Medicine_left'] + buy.iloc[0]['Aktivt_stof']
    user['Days_left'] = user['Medicine_left']/user['Daily_use']
    user['Money_spent'] = user['Money_spent'] + buy.iloc[0]['Price']
    #print(user)
    return user

log = []
def runSimulation(df, user, dates):
    for day in dates:
        user['Date'] = day
        user['Medicine_left'] = user['Medicine_left'] - user['Daily_use']
        user['Days_left'] = user['Days_left'] - 1
        #print(user)
        log.append(list(user.values()))
        if user['Medicine_left'] < user['Daily_use']:
            user = buyEvent(df, user, str(day))            
        else:
            pass  
    return log



log = runSimulation(b, user, everyday)
frame = pd.DataFrame(log, columns = ["Medicine_left", "Daily_use" , "Days_left", "Money_spent", "Dates"])

fig, ax = plt.subplots()
plt.plot( frame['Dates'], frame['Money_spent'])
#user = buyEvent(bd, user, "2016-11-21" ) 


'''
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
lol =[]    
for result in perdelta(date(2016, 11, 21), date(2022, 1, 10), timedelta(days=14)):
    lol.append(result)

filtered_df = bd[bd['Date'].isin(lol)]

loll = filtered_df[filtered_df['Price_pr_mg'].isin(filtered_df.groupby('Date').min()['Price_pr_mg'])]
loll['Aktivt_stof'].sum()-(800*1876)

'''



'''
print(stock)
stock = buyEvent(bd, stock, "2016-11-21" )
stock = buyEvent(bd, stock, "2018-12-17" )
stock = buyEvent(bd, stock, "2021-12-13" )
print(stock)
'''
'''
Test1: buy cheapest every 3 months

Test2 Buy cheapest the dey you run out

test3 buy cheapest 1 week before running out

test4 


def test1(bd, ):
    
    
'''

'''
df = pd.read_excel('lmpriser_eSundhed_220110.xlsx', sheet_name = "DATA")

bd = df[df['Lægemiddel'] == 'Pulmicort Turbuhaler']
bd['Doser'] = bd['Pakning'].apply(lambda x: float(x.split(' ')[0]))
bd['Styrke'] = bd['Styrke'].apply(lambda x: float(x.split(' ')[0]))
bd['Aktivt_stof'] = bd['Doser']*bd['Styrke']

bd = bd.melt(id_vars=["Varenummer", "Firma","Indikator", "Styrke", 'ATC', 'Form', 'Pakning', 'Lægemiddel', 'Aktivt_stof', 'Doser'], 
        var_name="Date", 
        value_name="Price")
bd.Date  = pd.to_datetime(bd['Date'], format='%Y%m%d')


bd.to_pickle('bd.pkl')
'''


