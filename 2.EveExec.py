#!/usr/bin/env python3
#This Program get the market close data for the pre-open stocks for that particular date
import pandas as pd
from datetime import date
from nsepy import get_history
#read the pre-open market file to get the stocks symbol
pom = pd.read_csv('pom.csv')
#create empty dataframe
hist = pd.DataFrame()
month = date.today().month
dt = int(input("enter the preopen market date "))
if dt == date.today().day:
    enddt = dt+1
else:
    enddt = dt
#get the history data for particular date ,change the end day to next day for getting live date data
for ind, row in pom.iterrows():
    name = row['symbol']
    hist = hist.append(get_history(symbol = name,start = date(2020,month,dt),end = date(2020,month,enddt)),ignore_index = True)
    print(row)

#delete the repeated values in history data
hist = hist.drop(['Symbol','Series','Prev Close','Open','Last','Deliverable Volume'],axis=1)
#concats the preopen 
pom = pd.concat([pom,hist],axis=1)
pom.to_csv("pom.csv",index=False)