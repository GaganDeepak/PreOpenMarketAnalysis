#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("pom.csv")

for ind, row in df.iterrows():
    df.loc[ind,'2daychng%'] = ((row['Close']-row['prevClose'])/row['prevClose'])*100
    df.loc[ind,'2dayhigh%'] = ((row['High']-row['open_price'])/row['open_price'])*100
    df.loc[ind,'2daylow%'] = ((row['open_price']-row['Low'])/row['open_price'])*100

for ind, row in df.iterrows():
    df.loc[ind,'swing%'] = (row['2dayhigh%']-row['2daylow%'])


for ind, row in df.iterrows():
    value = (row['swing%'])
    if value>0:
        df.loc[ind,'+ve'] = 1
    if value<0:
        df.loc[ind,'-ve'] = 1

df.to_csv("pom.csv",index=False)