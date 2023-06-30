
import datetime
import time
from datetime import date
import os
import sys

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

module_path = os.path.abspath(os.path.join('.')) 
sys.path.append(module_path+"\\data\\constant")

from constants import COMPANY_CODE

global previous_days, opening_days_filter

# 거래일과 거래일 바로 이전일의 변화율을 계산함.
def find_ratio(df_o, date_current):
    df_o_trans = df_o.transpose()
    df_o_trans.columns = ['before', 'after']
    df_o_trans['before'][df_o_trans['before'] == 0] = 1e-20 # 0으로 나누는 것을 예외로 두기 위하여 작은 숫자로 대체
    df_o_trans[date_current] = (df_o_trans['after'] - df_o_trans['before']) / df_o_trans['before']
    df_o_trans[date_current] = df_o_trans[date_current].apply(lambda x: float(f'{x:.5f}')) # 5 소수점까지
    df_o_trans[date_current] = df_o_trans[date_current].apply(lambda x: np.inf if x > 1e+10 else -np.inf if x < -1e+10 else x)
    # -inf, +inf로 대체함.
    return df_o_trans.transpose()

#
# 변화율(historical, investors), weekday를 계산하고 합하여 return함
def combine_data(opening_days_filter, df_inv, df_his):
    # df_inv : df_investor, df_his: df_historical
    investor_rate = pd.DataFrame()
    historical_rate = pd.DataFrame()
    date_weekday = pd.DataFrame()
    
    skip_num = 4 # -3 거래일전(-1 & -2 비교와 -1 & -3 비료)까지 계산하기 위하여 계산 시작은 4일째부터 시작

    for date_current in opening_days_filter[skip_num:]:
            
        date_previous_c = previous_days[0][date_current] # 이전 거래일(-1) 찾기

        # 거래 전날 요일 구하기 -------------------
        date_temp = {'date': date_current, 'weekday' : date_previous_c.weekday()}
        df_temp = pd.DataFrame(date_temp, index=[0]).set_index('date')
        date_weekday = pd.concat([date_weekday, df_temp], axis=0)
        # -----------------------------------------------
        
        # 거래 전날, 전전날을 확인하고 변화정도 계산하기(find_ratio)
        date_previous_1 = previous_days[0][date_previous_c]
        df_inv_comp_1 = df_inv.loc[[date_previous_1, date_previous_c]]
        df_his_comp_1 = df_his.loc[[date_previous_1, date_previous_c]]
    
    
        # 거래 전전일(-2일) 날짜 구하기
        date_previous_2 = previous_days[0][date_previous_1]
        # 거래 전전날(-2일째) 요일 구하기  -- 2일전 요일은 의미 없을 것 같아서 추가하지 않음.
#         date_temp_2 = {'date': date_current, 'weekday' : date_previous_2.weekday()}
#         df_temp_2 = pd.DataFrame(date_temp_2, index=[0]).set_index('date')
#         date_weekday = pd.concat([date_weekday, df_temp_2], axis=0)
        # 거래 전날(-1일), 전전날(-3일)을 확인하고 변화정도 계산하기(find_ratio)
        df_inv_comp_2 = df_inv.loc[[date_previous_2, date_previous_c]]
        df_his_comp_2 = df_his.loc[[date_previous_2, date_previous_c]]
            
        # 전날 -전전날 ratio, 전날 - 전전전날 ratio, column확대
        df_inv_concat_2 = pd.concat([find_ratio(df_inv_comp_1, date_current).iloc[[-1]],
                                 find_ratio(df_inv_comp_2, date_current).iloc[[-1]]], axis=1)
        df_his_concat_2 = pd.concat([find_ratio(df_his_comp_1, date_current).iloc[[-1]],
                                 find_ratio(df_his_comp_2, date_current).iloc[[-1]]], axis=1)
        
        investor_rate = pd.concat([investor_rate,  df_inv_concat_2], axis=0)
        historical_rate = pd.concat([historical_rate, df_his_concat_2], axis=0)

    total = pd.concat([investor_rate, historical_rate, date_weekday], axis=1)

    return total


# 개장일(date)과 이전 개장일(date_p1), 이전이전 개장일(date_p2)을 dict로 구성
def get_previous_days():
    base_data_directory = './data/base_data/stock_market_holydays/'
    opening_days_kor = pd.read_pickle(base_data_directory+'opening_days_kor.pkl') # 한국 개장일 데이터 
    df = pd.DataFrame(opening_days_kor)
    df['date_1'] = df['date'].shift(1)
    df['date_2'] = df['date'].shift(2)
    df['date_3'] = df['date'].shift(3)
    c_p1_dict = df.set_index('date').to_dict()['date_1'] # date로 date_p1 찾기
    c_p2_dict = df.set_index('date').to_dict()['date_2'] # date로 date_p2 찾기
    p1_c_dict = df.set_index('date_1').to_dict()['date'] # date_p1로 date 찾기
    p2_c_dict = df.set_index('date_2').to_dict()['date'] # date_p2로 date 찾기
    return c_p1_dict, c_p2_dict, p1_c_dict, p2_c_dict


code = COMPANY_CODE


# hist_column = [ 'date', 'open', 'high', 'low', 'close', 'close_cr', 'vol']
hist_column_m = [ 'date', 'open', 'high', 'low', 'close', 'vol'] # close_cr 제외하고 사용. divided by zero 회피용


# get stock market opening days
previous_days = get_previous_days()
opening_days_kor = list(previous_days[0].keys())


def find_start_date(df_investors_temp):
    start_date = datetime.date(2022, 1, 1) # 2022년 01월 01일 자료 있음. 추후 이전날짜 추가시 수정 필요
    for i in range(0, 360):
        sd_com = df_investors_temp['retail'].iloc[i]
        if sd_com != 0:
            start_date_com = df_investors_temp['date'].iloc[i] # 투자자별 자료가 있는 시작 날짜
            break
            
    if start_date <= start_date_com :
        return start_date_com
    else:
        return start_date


def is_opening_day(opening_day, date):
    if date in opening_day:
        return True
    else:
        return False


def get_previous_opening_day(opening_day, date):
    if date in opening_day:
        id = opening_day.index(date)
        return opening_day[id-1]
    else:
        p_date = date
        for _ in opening_day:
            p_date = p_date + datetime.timedelta(days=-1)
            if p_date in opening_day:
                return p_date
    raise("the date is not in the opening day")


# investor.pkl, historical.pkl. 읽기

directory_for_predict = './data/data_for_ml/predict/'
pkl_directory = './data/company_pkl/'
# base_data_directory = './data/base_data/stock_market_holydays/'
# opening_days_kor = pd.read_pickle(base_data_directory+'opening_days_kor.pkl') # 한국 개장일 데이터 
modification_time_his = pd.read_pickle(pkl_directory + 'modification_time_company_his.pkl')
modification_time_inv = pd.read_pickle(pkl_directory + 'modification_time_company_inv.pkl')

total = len(code)

for i, (key, val) in enumerate(code.items()):
 
    pkl_name= '{}_historical.pkl'.format(val[1])
    df_historical_temp = pd.read_pickle(pkl_directory + pkl_name)
    df_historical_temp = df_historical_temp[hist_column_m]
    
    # ---------historical 데이터 취득 날짜 시간 확인-------   
    dt_m_his = modification_time_his.loc[pkl_name][0] 
    hour_his = dt_m_his.hour
    minute_his = dt_m_his.minute
    #-------------------------------------------------------
    
    # close_cr 행을 없앰(변동이 없는 경우가 빌생하여 divided zero error 발생), close_cr은 target column에서 재 계산하여사용
    df_historical_temp['date'] = df_historical_temp['date'].dt.date # change to datetime
    
    pkl_name= '{}_investors.pkl'.format(val[1])
    df_investors_temp = pd.read_pickle(pkl_directory + pkl_name)
    df_investors_temp['date'] = df_investors_temp['date'].dt.date # change to datetime
    
    # ---------investors 데이터 취득 날짜 시간 확인-------   
    dt_m_inv = modification_time_inv.loc[pkl_name][0]
    hour_inv = dt_m_inv.hour
    minute_inv = dt_m_inv.minute
    # ------------------------------------------    
    
    # ******** 시작 일자, 마지막 일자  지정 ***********
#     start_date = datetime.date(2022, 1, 1) # 2022년 01월 01일 자료 있음. 추후 이전날짜 추가시 수정 필요
    start_date = find_start_date(df_investors_temp)
    end_date = df_investors_temp['date'].iloc[-1]  # 투자자별 자료가 있는 마지막 날짜
    if not is_opening_day(opening_days_kor, end_date):
        end_date = get_previous_opening_day(opening_days_kor, end_date)
        
    today = datetime.date.today()
    
    if ((end_date <= today) & (hour_his >= 16) & (hour_inv >= 16)): 
        # 그 이전에 common data를 받아 놓아야 함.
        end_date = opening_days_kor[opening_days_kor.index(end_date)+1] # 예측이 필요한 다가오는 개장일
    else:
        end_date = today
        
    # 실제 개장일로만 진행하기 위하여 date_range_ts를 재설정
    
    date_range_ts = pd.date_range(start=start_date, end=end_date).date #use .date fo convert timestamp to date.
    opening_days_filter = [item for item in date_range_ts if item in opening_days_kor] # 범위내에서 실제 거래일만 추출
    df_base = pd.DataFrame(pd.Series(opening_days_filter, name='date'))

    df_combined_temp = combine_data(opening_days_filter, 
                                             df_investors_temp.set_index('date'), 
                                             df_historical_temp.set_index('date'),
                                             )

    # column nama change according to the newly added columns
    column_name_change = ['retail_1', 'foreigner_1', 'institution_1', 'financial_1', 'invtrust_1', 'pension_1', 
          'privequity_1', 'bank_1', 'insurance_1', 'financeetc_1', 'corporateetc_1', 'foreigneretc_1', 
          'retail_2', 'foreigner_2', 'institution_2', 'financial_2', 'invtrust_2', 'pension_2', 
          'privequity_2', 'bank_2', 'insurance_2', 'financeetc_2', 'corporateetc_2', 'foreigneretc_2', 
          'open_1', 'high_1', 'low_1', 'close_1', 'vol_1', 
          'open_2', 'high_2', 'low_2', 'close_2', 'vol_2', 'weekday' ]
      
    df_combined_temp.columns = column_name_change
    
    df_combined_temp['temp'] = df_combined_temp['close_1'].shift(-1) # 현재날짜 증감을 확인하기 위하여 임시 컬럼 추가
    
    # 마지막 row의 temp는 None이기 때문에 0으로 처리하여 진행 (예측시 사용하지 않아 무관)
    # None을 0으로 변환, None을 남겨두면 무슨문제가 발생하나? 
    #       -> float와 비교가 되지 않아 에러발생
    ctemp = df_combined_temp['temp'].copy() 
    ctemp[-1] = 0
    df_combined_temp['temp'] = ctemp 
    # ------------------------------------

    min_rate = 0.0 # +로 끝난 상황을 알기 위함
    df_combined_temp['cr_00'] = df_combined_temp['temp'].map(lambda x : 1 if x > min_rate else 0)
    min_rate = 0.005 # 수수료등 비용 0.2672% 이상 확인하기 위함, 0.5% 상승 마감
    df_combined_temp['cr_05'] = df_combined_temp['temp'].map(lambda x : 1 if x >= min_rate else 0)
    min_rate = 0.010 # 1.0% 상승 마감
    df_combined_temp['cr_10'] = df_combined_temp['temp'].map(lambda x : 1 if x >= min_rate else 0)
    min_rate = 0.015 # 1.5% 상승 마감
    df_combined_temp['cr_15'] = df_combined_temp['temp'].map(lambda x : 1 if x >= min_rate else 0)
    min_rate = 0.020 # 2.0% 상승 마감
    df_combined_temp['cr_20'] = df_combined_temp['temp'].map(lambda x : 1 if x >= min_rate else 0)
    
    df_combined_temp.drop(columns='temp', inplace=True) # 사용후 삭제
    
    column_selected = column_name_change
    column_selected.extend(['cr_00', 'cr_05', 'cr_10', 'cr_15', 'cr_20'])  # 아래 class column 이 변경에 따라 수정해야 함
    
    globals()['df_{}_combined'.format(val[1])] = df_combined_temp.copy()
    globals()['df_{}_sel'.format(val[1])] = df_combined_temp[column_selected]
    
    # write company analysis data
    globals()['df_{}_sel'.format(val[1])].to_pickle(directory_for_predict + 'df_{}_company.pkl'.format(val[1]))
    globals()['df_{}_sel'.format(val[1])].to_csv(directory_for_predict + 'df_{}_company.csv'.format(val[1]))
    
    print(val[1], f'{i+1}/{total}', end=', ') # 진행상황 확인용
    sys.stdout.write(f'{val[1]}: {i+1}/{total}, ')
#    sys.stdout.flush()
