import datetime, time
from datetime import date

import pandas as pd

# 삼성전자 005930, 현대차 005380, 네이버 035420, KT&G 033780, 
# code = {'sec': '005930', 'hyunmotor': '005380', 'naver': '035420', 'ktng': '033780'}
code = {'sec': 'KR7005930003', 'hyunmotor': 'KR7005380001', 'naver': 'KR7035420009', 'ktng': 'KR7033780008'}

today_o = datetime.date.today()
today = today_o.strftime('%Y%m%d')
today_stock = today_o.strftime('%Y-%m-%d')

dir_name = 'data/company_daily_price_pkl/'
middle_name = '_10min_price_'

for key, val in code.items():
    f_name = dir_name+key+middle_name+today+'.pkl'
    df = pd.read_pickle(f_name)
    print('***{}***'.format(key))
    print(df.head(3))
    print(df.tail(3))