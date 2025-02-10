# from selenium import webdriver as wd
# from bs4 import BeautifulSoup as bs
import requests
import datetime, time
from datetime import date

import pandas as pd
import re
import os, sys

# import cfscrape  # Forbidden 403 발생시 requests 대신 사용
# scraper = cfscrape.create_scraper()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# 삼성전자 005930, 현대차 005380, 네이버 035420, KT&G 033780, 
code = {'sec': 'KR7005930003', 'hyunmotor': 'KR7005380001', 'naver': 'KR7035420009', 'ktng': 'KR7033780008'}

today_o = datetime.date.today()
today = today_o.strftime('%Y%m%d')
today_stock = today_o.strftime('%Y-%m-%d')
# code = {'sec': 'KR7005930003'}
# today='20240607'
# today_stock = '2024-06-07'

def get_data(ticker, today):
    url_base = 'https://stock.mk.co.kr/price/hourly?stock_code='
    for i in range(8):
        str1 = str(i+1)
        url = '{}{}{}{}{}{}'.format(url_base, ticker, '&day=', today, '&page=', str1)    
        # r = scraper.get(url, headers=headers)  
        r = requests.get(url, headers=headers)  
        html = r.content
        df1 = pd.read_html(html, attrs={"class": "table-stock line"}, flavor=["lxml", "bs4"])[0]
        if i == 0 :
            df = df1
        else:
            df=pd.concat([df,df1], ignore_index=True)
    return df

column_eng = ['date', 'price', 'change', 'change(%)', 'amount', 'volume']
column_kor = ['날짜', '현재가', '등락', '등락률(%)', '체결량', '거래량']

dir_name = 'data/company_daily_price_pkl/'
f_name = '_10min_price_'

for key, val in code.items():
    df = get_data(val, today_stock)
    df.columns = column_eng
    df_temp = df['date']
    yr = today[:4]
    df['date'] = df_temp.apply(lambda x : datetime.datetime.strptime(yr+x[:5], "%Y%m/%d"))
    df.insert(1, 'time', df_temp.apply(lambda x : datetime.datetime.strptime(x[-5:], "%H:%M").time()))
    filename = '{}{}{}{}.pkl'.format(dir_name, key, f_name, today) # code만 기입
    df.to_pickle(filename)
    filename = '{}{}{}{}.csv'.format(dir_name, key, f_name, today) # code만 기입
    df.to_csv(filename)