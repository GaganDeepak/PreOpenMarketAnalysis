#!/usr/bin/env python3
#This Program pomPDDWF(PreOpenMarketPreviousDayDataWithFormat)
import pandas as pd
from datetime import date,timedelta
from nsepy import get_history
#reads the nse file and formats to specific data type along with rename
pom = pd.read_csv("pom.csv",na_values=["-"],header=0,names=['symbol','prev_close','open_price','chng', '%Chng',
       'final_price', 'final_quantity', 'value', 'cap','52w_h', '52w_l'], thousands = ",")

#calculates total traded percentage in preopenmarket i.e (value/cap)*100
for ind, row in pom.iterrows():
    pom.loc[ind,"%traded"] = (row["value"]/row["cap"])*100

#removes excess data
pom = pom.drop(['prev_close','final_price','chng'],axis=1)

#create empty dataframe
hist = pd.DataFrame()
month = date.today().month
dt = int(input("enter the preopen market date "))
weekday = date(2020,month,dt).weekday()
if weekday>0 and dt>1:
    dt = dt-1
elif weekday==0 and dt>3:
    dt = dt-3
elif weekday == 0 and dt==3:
    dt = (date(2020,month,1)-timedelta(days=1)).day
elif weekday == 0 and dt==2:
    dt = (date(2020,month,1)-timedelta(days=2)).day
elif weekday == 0 and dt==1:
    dt = (date(2020,month,1)-timedelta(days=3)).day
    month = month-1
elif weekday>0 and dt==1:
    dt = (date(2020,month,1)-timedelta(days=1)).day
    month = month-1
print("fetching data for date:",dt,"/", month)
#get the history data of all nifty50 stocks for particular date(yyyy,mm,dd) enter previous date in both start and end
for ind, row in pom.iterrows():
    name = row['symbol']
    hist = hist.append(get_history(symbol = name,start = date(2020,month,dt),end = date(2020,month,dt)),ignore_index = True)
    print(row)

#delete the repeated values in history data
hist = hist.rename(columns={'High': 'prevHigh', 'Low': 'prevLow','Close' : 'prevClose','Open':'prevOpen'})
hist = hist.drop(['Symbol','Series','Prev Close','Deliverable Volume','Last'],axis=1)

#concats the preopen
pom = pd.concat([pom,hist],axis=1)

#Logic to compute before market open

#saves file to csv
pom.to_csv("pom.csv",index=False)

#checks the commonly traded stocks in 4 groups prints the data
pom = pom.sort_values(by="%Chng",ascending = False).reset_index(drop=True)
final_list = list(pom.loc[0:9,"symbol"])
pom = pom.sort_values(by="final_quantity",ascending = False).reset_index(drop=True)
final_list = final_list + list(pom.loc[0:9,"symbol"])
pom = pom.sort_values(by="%traded",ascending = False).reset_index(drop=True)
final_list = final_list + list(pom.loc[0:9,"symbol"])
pom = pom.sort_values(by="value",ascending = False).reset_index(drop=True)
final_list = final_list + list(pom.loc[0:9,"symbol"])
from collections import Counter
symbols = Counter(final_list) 
top_10 = symbols.most_common(10)

print("\n")
print(top_10)
print("\n")
temp = input("press any key to exit()")
exit()