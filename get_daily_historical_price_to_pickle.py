#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import requests
import datetime, time
from datetime import date

import pandas as pd
import re
import os, sys


# In[8]:


# 삼성전자 005930, 현대차 005380, 네이버 035420, KT&G 033780, 
# code = {'sec': '005930', 'hyunmotor': '005380', 'naver': '035420', 'ktng': '033780'}
code = {'sec': 'KR7005930003', 'hyunmotor': 'KR7005380001', 'naver': 'KR7035420009', 'ktng': 'KR7033780008'}
# code = {'sec': 'KR7005930003'}


# In[9]:


today_o = datetime.date.today()
today = today_o.strftime('%Y%m%d')
today_stock = today_o.strftime('%Y-%m-%d')


# In[10]:


def get_data(ticker, today):
    url_base = 'https://stock.mk.co.kr/price/hourly?stock_code='
#     url_base = 'https://stock.mk.co.kr/price/hourly?stock_code=KR7005930003&day=2023-01-25&page=2'
    for i in range(8):
        str1 = str(i+1)
        url = '{}{}{}{}{}{}'.format(url_base, ticker, '&day=', today, '&page=', str1)
        df1 = pd.read_html(url, attrs={"class": "table-stock line"}, flavor=["lxml", "bs4"])[0]
        if i == 0 :
            df = df1
        else:
#             df = df.append(df1) # append will be depreciated
            df=pd.concat([df,df1], ignore_index=True)
    return df


# In[11]:


column_eng = ['date', 'price', 'change', 'change(%)', 'amount', 'volume']
column_kor = ['날짜', '현재가', '등락', '등락률(%)', '체결량', '거래량']


# In[12]:


dir_name = 'data/company_daily_price_pkl/'
f_name = '_10min_price_'


# In[13]:


for key, val in code.items():
    df = get_data(val, today_stock)
    df.columns = column_eng
    df_temp = df['date']
    yr = today[:4]
    df['date'] = df_temp.apply(lambda x : datetime.datetime.strptime(yr+x[:5], "%Y%m/%d"))
    df.insert(1, 'time', df_temp.apply(lambda x : datetime.datetime.strptime(x[-5:], "%H:%M").time()))
    filename = '{}{}{}{}.pkl'.format(dir_name, key, f_name, today) # code만 기입
    df.to_pickle(filename)


# In[16]:


# aa = pd.read_pickle(dir_name+'sec_10min_price_20230207.pkl') # 저장 내용 확인


# In[ ]:




