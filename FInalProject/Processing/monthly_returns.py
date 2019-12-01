import numpy as np
import pandas as pd
import re
import datetime as dt
from pathlib import Path

def get_first_dates(data):
    data = data.loc[data.groupby(data.index.to_period('M')).apply(lambda x: x.index.min())]
    return data
    #https://stackoverflow.com/questions/48288059/how-to-get-last-day-of-each-month-in-pandas-dataframe-index-using-timegrouper (Zero)

def get_monthly_return(data):
    data = data[data['close'] != 0]
    data_monthly = data.apply(get_first_dates)
    df = pd.DataFrame(data_monthly[['ticker','stock','close']])
    df['monthly_return'] = df['close'].pct_change()
    df = df.dropna(axis=0, subset=['monthly_return'])
    df = df.reset_index()
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df = df.set_index(['date', 'ticker'], inplace=True)
    return df

def get_monthly_volume(data):
    monthly_volume = data.groupby([data.index.to_period('M'),'ticker'])['volume'].agg('sum')
    monthly_volume_usd = data.groupby([data.index.to_period('M'),'ticker'])['volume_usd'].agg('sum')
    df_monthly_volume = pd.DataFrame({'monthly_volume':monthly_volume, 'monthly_volume_usd':monthly_volume_usd})
    df_monthly_volume = df_monthly_volume.dropna(axis=0, subset=['monthly_volume'])
    df_monthly_volume  = df_monthly_volume.reset_index()
    df_monthly_volume['date'] = df_monthly_volume['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df_monthly_volume.set_index('date', inplace=True)
    return df_monthly_volume

def get_market_cap(data):
    data = data[data['close'] != 0]
    data_monthly = data.apply(get_first_dates)
    df_market_cap = pd.DataFrame({'ticker':data_monthly.ticker,'avg_market_cap':data_monthly.market_cap, 'avg_cap_floating':data_monthly.cap_floating})
    df_market_cap = df_market_cap.reset_index()
    df_market_cap['date'] = df_market_cap['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df_market_cap,set_index('date', inplace=True)
    return df_market_cap

#Loading dataset, and setting datetimeindex
home = str(Path.home())
read_name = home + '\\Desktop\\CUNY\\DATA608\\final\\bshare_sh_3yr.csv'
df = pd.read_csv(read_name, sep=';', encoding='UTF-8')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.set_index('date', inplace=True)
#df.info()

#Generating monthly volume, return, and market cap, then merging
mon_volume = get_monthly_volume(df)
mon_return = get_monthly_return(df)
mon_volume.set_index(['date', 'ticker'], inplace=True)
mon_return.set_index(['date', 'ticker'], inplace=True)
monthly_data = pd.merge(mon_volume,mon_return, left_index=True, right_index=True)
monthly_data = monthly_data.reindex(['stock', 'close', 'monthly_return', 'monthly_volume', 'monthly_volume_usd'], axis=1)
mon_market_cap = get_market_cap(df)
mon_market_cap.set_index(['date', 'ticker'], inplace=True)
monthly_data = pd.merge(monthly_data,mon_market_cap, left_index=True, right_index=True)
monthly_data.info()

#Adding market indices to dataset
ix000001 = pd.read_csv("C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\final\\write_csv\\000001.csv", sep=';',encoding='UTF-8')
ix000001['ticker'] = '000001'
ix000001['date'] = pd.to_datetime(ix000001['date'], format='%Y-%m-%d')
ix000001.set_index('date', inplace=True)
ix000001['volume_usd'] = ix000001['volume_dollars']
ix1_mon_return = get_monthly_return(ix000001)
ix1_mon_volume = get_monthly_volume(ix000001)
ix1_mon_return.set_index(['date', 'ticker'], inplace=True)
ix1_mon_volume.set_index(['date', 'ticker'], inplace=True)
ix1_monthly_data = pd.merge(ix1_mon_return,ix1_mon_volume, left_index=True, right_index=True)

ix000003 = pd.read_csv("C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\final\\write_csv\\000003.csv", sep=';',encoding='UTF-8')
ix000001['ticker'] = '000003'
ix000003['date'] = pd.to_datetime(ix000003['date'], format='%Y-%m-%d')
ix000003.set_index('date', inplace=True)
ix000003['volume_usd'] = ix000003['volume_dollars']
ix3_mon_return = get_monthly_return(ix000003)
ix3_mon_volume = get_monthly_volume(ix000003)
ix3_mon_return.set_index(['date', 'ticker'], inplace=True)
ix3_mon_volume.set_index(['date', 'ticker'], inplace=True)
ix3_monthly_data = pd.merge(ix3_mon_return,ix3_mon_volume, left_index=True, right_index=True)

monthly_data = monthly_data.append(ix1_monthly_data)
monthly_data = monthly_data.append(ix3_monthly_data)

monthly_data.to_csv('C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\final\\write_csv\\monthly_returns.csv', sep=';', encoding='UTF-8')


# monthly_data.sort_values('avg_market_cap',ascending=False)
# monthly_data[monthly_data.avg_market_cap == max(monthly_data.avg_market_cap)]
# monthly_data[monthly_data.monthly_volume_usd == max(monthly_data.monthly_volume_usd)]



