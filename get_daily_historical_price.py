
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import requests
import datetime, time
from datetime import date

import pandas as pd
import re
import os, sys


# 삼성전자 005930, 현대차 005380, 네이버 035420, KT&G 033780, 
code = {'sec': '005930', 'hyunmotor': '005380', 'naver': '035420', 'ktng': '033780'}


today = datetime.date.today()
today = today.strftime('%Y%m%d')


def get_data(ticker):
    for i in range(3):
        str1 = str(i+1)
        url = '{}{}{}{}'.format('https://vip.mk.co.kr/newSt/price/minprice.php?type=10&stCode=', ticker, '&p_page=', str1)
        df1 = pd.read_html(url, attrs={"class": "table_3"}, flavor=["lxml", "bs4"])[0]
        if i == 0 :
            df = df1
        else:
            df = df.append(df1)
    return df


column_eng = ['date', 'price', 'change', 'change(%)', 'amount', 'volume']
column_kor = ['날짜', '현재가', '등락', '등락률(%)', '체결량', '거래량']

dir_name = 'c:/jupyter연습/factors_affecting_stock_price/data/stocks/daily_price/'
f_name = '_10min_price_'


for key, val in code.items():
    df = get_data(val)
    df.columns = column_eng
    df_temp = df['date']
    yr = today[:4]
    df['date'] = df_temp.apply(lambda x : datetime.datetime.strptime(yr+x[:5], "%Y%m/%d"))
    df.insert(1, 'time', df_temp.apply(lambda x : datetime.datetime.strptime(x[-5:], "%H:%M").time()))
    filename = '{}{}_{}{}{}.csv'.format(dir_name, val, key, f_name, today)
    df.to_csv(filename, index=False)





