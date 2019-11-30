import numpy as np
import pandas as pd
import re
import datetime as dt
from pathlib import Path
home = str(Path.home())

def clean_df(df):
    df['Div_2019_date'] = df['Div_2019_date'].apply(clean_date) 
    df['Div_2018_date'] = df['Div_2018_date'].apply(clean_date) 
    df['Div_2017_date'] = df['Div_2017_date'].apply(clean_date) 
    df['Div_2016_date'] = df['Div_2016_date'].apply(clean_date) 
    return df

def clean_date(d):
    return dt.datetime.strptime(d, '%Y-%m-%d')

file_name = 'dividends_sh.xls'
read_name = home + '\\Desktop\\CUNY\\DATA608\\final\\dividends_sh.csv'
df = pd.read_csv(read_name, sep=';', encoding='UTF-8')

#df = clean_df(df)
write_name = home + '\\Desktop\\CUNY\\DATA608\\final\\write_csv\\dividends_sh.csv'
df.to_csv(write_name, sep=';', encoding='UTF-8')
