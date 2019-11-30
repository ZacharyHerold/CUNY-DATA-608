file_name = '900901.csv'

import numpy as np
import pandas as pd
import re
import datetime as dt
from pathlib import Path
home = str(Path.home())

def clean_df(df):
    df.columns = ["date","ticker","stock","close","high","low","open","price_change","volume","volume_usd","market_cap","cap_floating"]
    #np.round(df[["close","high","low","open","price_change"]], decimals=4)
    df['date'] = df['date'].apply(clean_date) 
    df['ticker'] = df['ticker'].apply(clean_ticker) 
    #df = df.drop(['stock'], axis=1)
    #df['price_change'] = df['price_change'].apply(clean_pricechange) 
    df.set_index('date', inplace=True)
    df = df.reindex(index=df.index[::-1])
    return df

def clean_ticker(t):
    return t[1:]

def clean_date(d):
    return dt.datetime.strptime(d, '%Y-%m-%d')

def clean_pricechange(p):
    return float(p)

read_name = home + '\\Desktop\\CUNY\\DATA608\\final\\read_csv\\' + file_name
df = pd.read_csv(read_name, encoding='gb2312')
df.info()

#df = pd.read_csv(read_name, encoding='UTF-8')
df = clean_df(df)
write_name = home + '\\Desktop\\CUNY\\DATA608\\final\\write_csv\\' + file_name
df.to_csv(write_name, sep=';', encoding='UTF-8')
