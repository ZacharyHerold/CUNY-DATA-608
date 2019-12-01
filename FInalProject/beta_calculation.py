import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\final\\write_csv\\monthly_returns.csv', sep=';', encoding='UTF-8')
d = {"'000003":'000003'}
df = df.replace(d)
df = df[df.ticker != '000001']
df.info()

ix = df[df.ticker == '000003']

def ix_align_months(stock_data, index_data):
    date_list = list(stock_data.date)
    ix_sub = index_data[index_data.date.isin(date_list)]
    return ix_sub

def calculate_beta(ticker, ix=ix):
    stock_sub = df[df.ticker == ticker]
    ix_aligned = ix_align_months(stock_sub, ix)
    cov_mat = np.cov(stock_sub.monthly_return, ix_aligned.monthly_return)
    beta = cov_mat[0][1]/cov_mat[1][1]
    return ticker, beta 

tickers = list(set(df.ticker))
b = list(map(calculate_beta, tickers))
stock_summary = pd.DataFrame(b, columns=['ticker', 'beta'])
stock_summary.set_index('ticker', inplace=True)

temp1 = df.groupby('ticker')['avg_market_cap'].mean()
temp2 = df.groupby('ticker')['monthly_volume'].mean()
temp3 = df.groupby('ticker')['monthly_volume_usd'].mean()

df.info()
df.monthly_return[df.ticker=="900902"]
df.iloc[0]

def calculate_sharpe(ticker, data=df):
    returns_plus_one = df[df.ticker==ticker]['monthly_return'].add(1)
    cumulative_return = returns_plus_one.cumprod()
    std = np.std(df[df.ticker==ticker]['monthly_return'])
    return cumulative_return / std

df_temp = pd.DataFrame({'avg_market_cap':temp1,'avg_volume':temp2, 'avg_volume_usd':temp3})
stock_summary2 = stock_summary.merge(df_temp, left_index=True, right_index=True)
stock_summary2.info()

plt.scatter(stock_summary2.beta, stock_summary2.avg_market_cap)
plt.show()