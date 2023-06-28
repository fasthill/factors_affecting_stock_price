
import datetime
import time
from datetime import date

import pickle

import pandas as pd
import numpy as np

import os
import sys
import shutil

import matplotlib.pyplot as plt

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as bs
import requests

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

time.sleep(1)
driver = wd.Chrome()

def pick_date_in_calendar(start_date, end_date):
    driver.find_element(By.CLASS_NAME, 'DatePickerWrapper_icon__Qw9f8').click()

    start = driver.find_elements(By.CLASS_NAME, 'NativeDateInput_root__wbgyP')[0]
    end = driver.find_elements(By.CLASS_NAME, 'NativeDateInput_root__wbgyP')[1]

    start_element = start.find_element(By.CSS_SELECTOR, 'input[type=date]')
    end_element = end.find_element(By.CSS_SELECTOR, 'input[type=date]')

    start_element.clear()
    start_element.send_keys(start_date)
    start_element.click()

    end_element.clear()
    end_element.send_keys(end_date)
    end_element.click()

    driver.find_element(By.CLASS_NAME, 'inv-button.HistoryDatePicker_apply-button__fPr_G').click()
    
    end_date_in_table = datetime.datetime.strptime(start_date, '%Y-%m-%d').date().strftime('%m/%d/%Y')
    css_sel = '#__next > div.desktop\:relative.desktop\:bg-background-default > div > div > div.grid.gap-4.tablet\:gap-6.grid-cols-4.tablet\:grid-cols-8.desktop\:grid-cols-12.grid-container--fixed-desktop.general-layout_main__lRLYJ > main > div > div:nth-child(5) > div > div > div.border.border-main > div > table > tbody'  
    WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_sel), end_date_in_table))
    
    return

def get_table_df(start_date_range, end_date_range):

   pick_date_in_calendar(start_date_range, end_date_range)

   table_class = 'datatable_table__D_jso datatable_table--border__B_zW0 datatable_table--mobile-basic__W2ilt datatable_table--freeze-column__7YoIE'
   df = pd.read_html(driver.page_source, attrs={"class": table_class}, flavor=["lxml", "bs4"])[0]

   df['Date'] = df['Date'].apply(lambda x : datetime.datetime.strptime(x, "%m/%d/%Y").date())
   df = df.sort_values(by='Date').reset_index(drop=True) # ascending order and renumbering index starting 0.
   
   return df

def save_dataframe(df, pkl_name):
    pkl_directory = 'data/common_pkl/'
    df.to_pickle(pkl_directory+pkl_name)
    df.to_csv(pkl_directory+pkl_name.replace('pkl','csv'))
    return

start_date = '2021-12-20'
today = datetime.date.today()
today_str = today.strftime('%Y-%m-%d')

us_bond_10yr_url = 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'
driver.get(us_bond_10yr_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

us_10yr = ['date', 'bond_usa_10', 'open', 'high', 'low', 'bond_usa_10_cr']
df.columns = us_10yr

pkl_name = 'us_10yr_bond.pkl'

save_dataframe(df, pkl_name)

print("us_bond_10yr, len:", len(df))

us_bond_2yr_url = 'https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield-historical-data'
driver.get(us_bond_2yr_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

us_2yr = ['date', 'bond_usa_2', 'open', 'high', 'low', 'bond_usa_2_cr']
df.columns = us_2yr

pkl_name = 'us_2yr_bond.pkl'

save_dataframe(df, pkl_name)

print("us_bond_2yr, len:", len(df))

us_bond_3mon_url = 'https://www.investing.com/rates-bonds/u.s.-3-month-bond-yield-historical-data'
driver.get(us_bond_3mon_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

us_3mon = ['date', 'bond_usa_3m', 'open', 'high', 'low', 'bond_usa_3m_cr']

df.columns = us_3mon

pkl_name = 'us_3mon_bond.pkl'

save_dataframe(df, pkl_name)

print("us_bond_3mon, len:", len(df))

kosdaq_url = 'https://www.investing.com/indices/kosdaq-historical-data'
driver.get(kosdaq_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

kosdaq = ['date', 'kosdaq', 'open', 'high', 'low', 'volume', 'kosdaq_cr']

df.columns = kosdaq

pkl_name = 'kosdaq.pkl'

save_dataframe(df, pkl_name)

print("kosdaq, len:", len(df))

kospi_url = 'https://www.investing.com/indices/kospi-historical-data'
driver.get(kospi_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

kospi = ['date', 'kospi', 'open', 'high', 'low', 'volume', 'kospi_cr']

df.columns = kospi

pkl_name = 'kospi.pkl'

save_dataframe(df, pkl_name)

print("kospi, len:", len(df))

snp_futures_url = 'https://www.investing.com/indices/us-spx-500-futures-historical-data'
driver.get(snp_futures_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

snp_future = ['date', 'spx_f', 'open', 'high', 'low', 'volume', 'spx_f_cr']

df.columns = snp_future

pkl_name = 'snp_future.pkl'

save_dataframe(df, pkl_name)

print("snp_futures, len:", len(df))

nas_futures_url = 'https://www.investing.com/indices/nq-100-futures-historical-data'
driver.get(nas_futures_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

ixic_future = ['date', 'ixic_f', 'open', 'high', 'low', 'volume', 'ixic_f_cr']

df.columns = ixic_future

pkl_name = 'ixic_future.pkl'

save_dataframe(df, pkl_name)

print("nas_futures, len:", len(df))

dow_futures_url = 'https://www.investing.com/indices/us-30-futures-historical-data'
driver.get(dow_futures_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

dji_future = ['date', 'dji_f', 'open', 'high', 'low', 'volume', 'dji_f_cr']

df.columns = dji_future

pkl_name = 'dji_future.pkl'

save_dataframe(df, pkl_name)

print("dow_futures, len:", len(df))

wti_futures_url = 'https://www.investing.com/commodities/crude-oil-historical-data'
driver.get(wti_futures_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Vol.'] = df['Vol.'].str[:-1].astype('float')
df['Change %'] = df['Change %'].str[:-1].astype('float')

wti_future = ['date', 'wti', 'open', 'high', 'low', 'volume', 'wti_cr']

df.columns = wti_future

pkl_name = 'wti_future.pkl'

save_dataframe(df, pkl_name)

print("wti_futures, len:", len(df))

dollar_index_url = 'https://www.investing.com/indices/usdollar-historical-data'
driver.get(dollar_index_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

dxy_future = ['date', 'dxy', 'open', 'high', 'low', 'volume', 'dxy_cr']

df.columns = dxy_future

pkl_name = 'dxy_future.pkl'

save_dataframe(df, pkl_name)

print("dollar_index, len:", len(df))


ixf_url = 'https://www.investing.com/indices/nasdaq-financial-100-historical-data'
driver.get(ixf_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

ixf = ['date', 'ixf', 'open', 'high', 'low', 'volume', 'ixf_cr']

df.columns = ixf

pkl_name = 'ixf.pkl'

save_dataframe(df, pkl_name)

print("nasdaq-financial-100, len:", len(df))


qnet_url = 'https://www.investing.com/indices/nasdaq-internet-historical-data'
driver.get(qnet_url)
time.sleep(1)

df = get_table_df(start_date, today_str)

df['Change %'] = df['Change %'].str[:-1].astype('float')

qnet = ['date', 'qnet', 'open', 'high', 'low', 'volume', 'qnet_cr']

df.columns = qnet

pkl_name = 'qnet.pkl'

save_dataframe(df, pkl_name)

print("nasdaq-internet, len:", len(df))


driver.close()
driver.quit()

