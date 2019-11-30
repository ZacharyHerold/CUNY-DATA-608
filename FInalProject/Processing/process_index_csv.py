#################################################
# Index Loading and Manipulation
# 上证指数(000001) && B股指数(000003)
# From http://quotes.money.163.com/trade/lsjysj_zhishu_000003.html

import numpy as np
import pandas as pd
import re
import datetime as dt
from pathlib import Path
home = str(Path.home())

b_idx = pd.read_csv('C:\\Users\\zhero\\Desktop\\CUNY\\DATA608\\final\\read_csv\\000001.csv',encoding='gb2312')
#Index(['日期', '股票代码', '名称', '收盘价', '最高价', '最低价', '开盘价', '前收盘', '涨跌额', '涨跌幅', '成交量', '成交金额']
b_idx.info()
b_idx.columns=['date','ticker','stock','close','high','low','open','price_change','volume','volume_dollars']
b_idx['date'] = pd.to_datetime(b_idx['date'], format='%Y-%m-%d')
b_idx.set_index('date', inplace=True)

write_name = home + '\\Desktop\\CUNY\\DATA608\\final\\write_csv\\000001.csv'
b_idx.to_csv(write_name, sep=';', encoding='UTF-8')

