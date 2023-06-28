
from selenium import webdriver as wd
from selenium.webdriver import ActionChains # scroll down 사용하기 위하여 선서
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as bs

import datetime, time
from datetime import date

import pandas as pd
import numpy as np
import requests
import time
import os, sys

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

module_path = os.path.abspath(os.path.join('.')) 
sys.path.append(module_path+"\\data\\constant")

from constants import COMPANY_CODE

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
driver = wd.Chrome()

def get_data_company(com_name):

    com_ticker = com_name[:6]
    # 회사이름 입력 Q 버튼
    driver.find_element(By.CSS_SELECTOR, '#btnisuCd_finder_stkisu0_0').click()
    time.sleep(2)

    # pop up된 입력창에서 회사이름 입력
    driver.find_element(By.ID, 'searchText__finder_stkisu0_0').clear()
    time.sleep(1)

    driver.find_element(By.ID, 'searchText__finder_stkisu0_0').send_keys(com_name)
    time.sleep(2)

    # 검색 버튼 푸시
    driver.find_element(By.CSS_SELECTOR, '#searchBtn__finder_stkisu0_0').click()
    time.sleep(2)

    # 테이블에서 최종 선택
    css_sel = '#jsGrid__finder_stkisu0_0 > tbody > tr:nth-child(1) > td:nth-child(1)'

    element = WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_sel), com_ticker))
    # 위 라인은 pop up 창이 사라질 때까지 기다리게 해 줌
    driver.find_element(By.CSS_SELECTOR, css_sel).click()
    time.sleep(2)

    return


def set_date(start_date, end_date): # 일정 기간 데이터 취득
    # end_date를 먼저 입력하고 start date 입력. 반대로 하면 start date가 이전날짜로  reset되어짐
    driver.find_element(By.ID, 'endDd').clear()
    driver.find_element(By.ID, 'endDd').send_keys(end_date)
    time.sleep(1)
    
    driver.find_element(By.ID, 'strdDd').clear()
    driver.find_element(By.ID, 'strdDd').send_keys(start_date)
    time.sleep(1)


def get_data(start_date, end_date):
    
    column_name = ['date', 'close', 'change', 'close_cr', 'open', 'high', 'low', 
                  'vol', 'vol_amount','total_amount', 'total_counts' ]
    # ['일자', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', 
    #                                 '거래대금', '시가총액', '상장주식수']
 
    start_str = start_date.strftime('%Y-%m-%d')
    ed_str = end_date.strftime('%Y-%m-%d')
    set_date(start_str, ed_str)

    # 테이블  취득 버튼 클릭 (우상귀)
    driver.find_element(By.ID, 'jsSearchButton').click()
    time.sleep(5)

    df = pd.read_html(driver.page_source, 
                          attrs={"class": "CI-GRID-BODY-TABLE"}, flavor=["lxml", "bs4"])[0]
    df.columns = column_name
    df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%Y/%m/%d"))
    df_get = df[['date', 'open', 'high', 'low', 'close', 'close_cr', 'vol']]
    
    return df_get


def non_empty_index_df(df_input, start_date, end_date): # 토,일,공휴일등 거래가 없는 일자도 모두 포함
    date_range_ts = pd.date_range(start=start_date, end=end_date)
    df_input.set_index('date', inplace=True)
    df_out = pd.DataFrame(columns = df_input.columns)
    df_out.insert(0, 'date', date_range_ts)
    df_out.set_index('date', inplace=True)
    df_out.update(df_input)
    df_out.reset_index(inplace=True)
    return df_out


def concat_df(df_o, df):
    df_o = pd.concat([df_o, df], ignore_index=True)
    df_o.drop_duplicates(subset=['date'], keep='last', inplace=True)
    df_o.sort_values(by=[df_o.columns[0]], inplace=True)
    df_o.index = np.arange(0, len(df_o))  # 일련 번호 오름차순으로 재 설정
    return df_o


# 개장일이 아닌 row는 삭제하기 위하여 개장일 데이터 load
base_data_directory = './data/base_data/stock_market_holydays/'
opening_days_kor = pd.read_pickle(base_data_directory+'opening_days_kor.pkl') # 한국 개장일 데이터 

# df_in : common data, opening_days : Series from oprning_days_xxx.pkl
def select_openingdays(df_in, opening_days):
    df_sel = df_in['date'].apply(lambda x: True if x.date() in list(opening_days) else False)
    df_out = df_in[df_sel].reset_index(drop=True)
    return df_out


# driver.set_window_position(-10000,0) # hide windows
main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
# 개별종목 시세추이 data-menu-id: MDC0201020103
driver.get(main_url)
time.sleep(1)


# 백만원 단위 표시 선정
css_sel = '#MDCSTAT017_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) \
           > select.CI-MDI-UNIT-MONEY > option:nth-child(3)'
driver.find_element(By.CSS_SELECTOR, css_sel).click()
time.sleep(1)


code = COMPANY_CODE


pkl_directory = 'data/company_pkl/'
modification_time = pd.read_pickle(pkl_directory + 'modification_time_company_his.pkl')
total = len(code)

for i, (key, val) in enumerate(code.items()):
    com_name = "/".join([key, val[0]])
    pkl_name= '{}_historical.pkl'.format(val[1])
    try :
        df_o = pd.read_pickle(pkl_directory + pkl_name)
        start_date = df_o['date'].iloc[len(df_o)-1]
    except :
        start_date = datetime.date(2022, 1, 1)   # 데이터 취득 시작 일자     

#     start_date = datetime.date(2023, 5, 11)  # 데이터 취득 오류시 일시 사용
        
    end_date = datetime.date.today()
    get_data_company(com_name)
    df_get = get_data(start_date, end_date)
    df_out = non_empty_index_df(df_get, start_date, end_date)
#   NaN to null string. cause NaN does not replace original values in the original datafram    
    try :
        df_o = concat_df(df_o, df_out) # append df to original df
    except :
        df_o = df_out.copy()
        
    # 개장일이 아닌 row는 삭제
    df_o = select_openingdays(df_o, opening_days_kor)
    
    df_o.replace(np.nan, '', inplace=True)
    df_o.to_pickle(pkl_directory+pkl_name)
    df_o.to_csv(pkl_directory+pkl_name.replace('pkl','csv'))
    modification_time.loc[pkl_name][0] = datetime.datetime.now()
    
    print(com_name, f'{i+1}/{total}', end=', ') # 진행상황 확인용
    
modification_time.to_pickle(pkl_directory+'modification_time_company_his.pkl')
modification_time.to_csv(pkl_directory+'modification_time_company_his.csv')


def date_set(datei): # 하루 하루 데이터를 받아야 함.
# end_date를 먼저 입력하고 start date 입력. 반대로 하면 start date가 이전날짜로  reset되어짐
    driver.find_element(By.ID, 'endDd').clear()
    driver.find_element(By.ID, 'endDd').send_keys(datei)
    time.sleep(1)
    driver.find_element(By.ID, 'strtDd').clear()
    driver.find_element(By.ID, 'strtDd').send_keys(datei)
    time.sleep(1)
    return


def push_button_1(): # 조회 button push
    xp = '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/a' 
    # use full xpath to avoid 'Message: element not interactable' Error
    driver.find_element(By.XPATH, xp).click()
    time.sleep(1) # 여유시간 배분
    css_sel = 'div.loading-bar-wrap.small' # 각기 다른 loading 페이지에서 공통적으로 사용됨
    element = WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css_sel)))
    # 위 라인은 pop up 창이 사라질 때까지 기다리게 해 줌
    time.sleep(1) # 여유시간 배분
    return


base_data_directory = './data/base_data/stock_market_holydays/'
opening_days_kor = pd.read_pickle(base_data_directory+'opening_days_kor.pkl') # 한국 개장일 데이터 
def is_opening_day(date): # 개장일 확인
    date = datetime.datetime.strptime(date, "%Y%m%d").date()
    if date in list(opening_days_kor):
        return True
    else:
        return False


index_name = ['investor', 'sell_quantity', 'buy_quantity', 'pure_buy_quantity', 'sell', 'buy', 'pure_buy']
column_name = ['financial', 'insurance', 'invtrust', 'privequity', 'bank', 'financeetc', 'pension',
              'institution', 'corporateetc', 'retail', 'foreigner', 'foreigneretc', 'total' ]
def get_daily_data(date_range):
    df_org = None
    for datei in date_range: 
        
        if not is_opening_day(datei): # 나중(5월 2일 이후)에 개장일만 수집하도록 수정할 것
            continue

        date_set(datei)
        push_button_1()
        df = pd.read_html(driver.page_source, 
                          attrs={"class": "CI-GRID-BODY-TABLE"}, flavor=["lxml", "bs4"])[0]
        df.columns = index_name
        df_new = df[['investor', 'pure_buy']] # 순매수 금액
        df_new.set_index('investor', inplace=True)
        dft = df_new.T
        dft.columns = column_name
        dft.insert(0, "date", datetime.datetime.strptime(datei, "%Y%m%d"))
        dft.reset_index(drop=True, inplace=True)
        if df_org is None:
            df_org = dft.copy()
            continue
#         df_org = df_org.append(dft, ignore_index=True) # append will be depreciated
        df_org =pd.concat([df_org,dft], ignore_index=True)
        
    return df_org


def get_data_company_investor(com_name, start_date, end_date):
    
    com_ticker = com_name[:6]
    # 회사이름 입력 Q 버튼
    driver.find_element(By.CSS_SELECTOR, '#btnisuCd_finder_stkisu0_1').click()
    time.sleep(2)

    # pop up된 입력창에서 회사이름 입력
    driver.find_element(By.ID, 'searchText__finder_stkisu0_1').clear()
    time.sleep(1)
    
    driver.find_element(By.ID, 'searchText__finder_stkisu0_1').send_keys(com_name)
    time.sleep(2)

    # 검색 버튼 푸시
    driver.find_element(By.CSS_SELECTOR, '#searchBtn__finder_stkisu0_1').click()
    time.sleep(2)

    # 테이블에서 최종 선택
    css_sel = '#jsGrid__finder_stkisu0_1 > tbody > tr:nth-child(1) > td:nth-child(1)'

    element = WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_sel), com_ticker))
    driver.find_element(By.CSS_SELECTOR, css_sel).click()
    time.sleep(2)
    
    date_range = convert_date(start_date, end_date)
    return get_daily_data(date_range)


def convert_date(start_date, end_date):
    date_range_ts = pd.date_range(start=start_date, end=end_date)
    date_range = []
    for x in date_range_ts:
        date_range.append(datetime.datetime.strftime(x, "%Y%m%d"))
    return date_range


# 투자자별 URL로 변경
main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203'
driver.get(main_url)
time.sleep(2)


# Message: element not interactable Error 방지용. 클릭하기 위하여는 그 위치가 클릭할 수 있게 노출되어 있어야 함
# 투자자별 거래실적 버튼이 위치한 곳으로 화면 scroll 

# id가 jsOpenView_1 인 element 를 찾음
stop_tag = driver.find_element(By.ID, 'jsOpenView_1')

# jsOpenView_1 element 까지 스크롤
action = ActionChains(driver)
action.move_to_element(stop_tag).perform()

# 투자자별 거래 실적 버튼 클릭
driver.find_element(By.ID, 'jsOpenView_1').click()
time.sleep(2)


# 백만원 단위 표시 선정
css_sel = '#MDCSTAT023_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > select.CI-MDI-UNIT-MONEY > option:nth-child(3)'

driver.find_element(By.CSS_SELECTOR, css_sel).click()
time.sleep(1)


pkl_directory = 'data/company_pkl/'
# modification_time = {} # 데이터가 생성된 시간 저장 dictionary
modification_time = pd.read_pickle(pkl_directory + 'modification_time_company_inv.pkl')
total = len(code)

for i, (key, val) in enumerate(code.items()):
    com_name = "/".join([key, val[0]])
    pkl_name= '{}_investors.pkl'.format(val[1])
    try :
        df_o = pd.read_pickle(pkl_directory + pkl_name)
        start_date = df_o['date'].iloc[len(df_o)-1]
    except :
        start_date = datetime.date(2022, 1, 1)   # 데이터 취득 시작 일자 
        
#     start_date = datetime.date(2023, 5, 11) # 데이터 취득 오류시 일시 사용

    end_date = datetime.date.today()
    df_out = get_data_company_investor(com_name, start_date, end_date)
    try :
        df_out = df_out[df_o.columns]     
        df_o = concat_df(df_o, df_out) # append df to original df
    except :
        df_col = ['date', 'retail', 'foreigner', 'institution', 'financial', 'invtrust',
                  'pension', 'privequity', 'bank', 'insurance', 'financeetc',
                  'corporateetc', 'foreigneretc']
        df_out = df_out[df_col]
        df_o = df_out.copy()
        
    # 개장일이 아닌 row는 삭제
    df_o = select_openingdays(df_o, opening_days_kor)
    
    df_o.to_pickle(pkl_directory+pkl_name)
    df_o.to_csv(pkl_directory+pkl_name.replace('pkl','csv'))
    modification_time.loc[pkl_name][0] = datetime.datetime.now()
    
    print(com_name, f'{i+1}/{total}', end=', ') # 진행상황 확인용
    
modification_time.to_pickle(pkl_directory+'modification_time_company_inv.pkl')
modification_time.to_csv(pkl_directory+'modification_time_company_inv.csv')


driver.close()
driver.quit()
