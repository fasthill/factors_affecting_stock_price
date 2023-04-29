code_all = {'005930' : ['삼성전자', 'sec'], '373220' : ['LG에너지솔루션', 'lgenergy'], 
        '000660' : ['SK하이닉스', 'skhynix'], '207940' : ['삼성바이오로직스', 'ssbio'],
        '006400' : ['삼성SDI', 'sdi'], '051910' : ['LG화학', 'lgchemical'],
        '005935' : ['삼성전자우', 'secpre'], '005380' : ['현대차', 'hyunmotor'],
        '035420' : ['NAVER', 'naver'], '000270' : ['기아','kia'],
        '035720' : ['카카오', 'kakao'], '005490' : ['POSCO홀딩스', 'poscoholding'],
        '105560' : ['KB금융', 'kbbank'], '028260' : ['삼성물산', 'sscnt'],
        '068270' : ['셀트리온', 'celltrion'], '012330' : ['현대모비스', 'mobis'],
        '055550' : ['신한지주', 'shgroup'], '066570' : ['LG전자', 'lgelec'],
        '003670' : ['포스코퓨처엠', 'poscochemical'], '096770' : ['SK이노베이션', 'skinnovation'],
        '033780' : ['KT&G', 'ktng'], '030200' : ['KT', 'kt'],
        '003550' : ['LG', 'lg'], '034730' : ['SK', 'sk'], 
        '032830' : ['삼성생명', 'sslife'], '086790' : ['하나금융지주', 'hana'], 
        '009150' : ['삼성전기', 'sselec'], '015760' : ['한국전력', 'koreaelec'],
        '034020' : ['두산에너빌리티', 'doosanener'], '010130' : ['고려아연', 'koreazinc'],
        '017670' : ['SK텔레콤', 'sktelecom'], '011200' : ['HMM', 'hmm'],
        '000810' : ['삼성화재', 'ssfire'], '051900' : ['LG생활건강', 'lglife'],
        '010950' : ['S-Oil', 'soil'], '259960' : ['크래프톤', 'crafton'],
        '018260' : ['삼성에스디에스', 'sds'], '329180' : ['현대중공업', 'hhi'],
        '003490' : ['대한항공', 'koreanair'], '036570' : ['엔씨소프트', 'ncsoft'],
        '009830' : ['한화솔루션', 'hanhwasol'], '316140' : ['우리금융지주', 'woorifg'],
        '090430' : ['아모레퍼시픽', 'amore'], '011170' : ['롯데케미칼', 'lottechem'], 
        '024110' : ['기업은행', 'ibk'], '138040' : ['메리츠금융지주', 'meritz'], 
        '377300' : ['카카오페이', 'kakaopay'], '011070' : ['LG이노텍', 'lginnotek'],
        '028050' : ['삼성엔지니어링', 'ssengineering'], '361610' : ['SK아이이테크놀로지', 'skietech'],
        '086280' : ['현대글로비스', 'glovis'], '302440' : ['SK바이오사이언스', 'skbio'],}

code_4 = {'005930': ['삼성전자', 'sec'], '005380': ['현대차', 'hyunmotor'],
                 '035420': ['NAVER', 'naver'], '033780': ['KT&G', 'ktng']}

common_files = [ "dji.pkl", "dji_future.pkl", "dxy_future.pkl", 
               "ixic_future.pkl", "kor_10yr_bond.pkl",
              "kor_2yr_bond.pkl", "kosdaq.pkl", "kospi.pkl", "krw_rate.pkl", "nas.pkl",
              "snp_future.pkl", "sox.pkl", "spx.pkl", "us_10yr_bond.pkl", "us_2yr_bond.pkl",
              "us_3mon_bond.pkl", "vix.pkl", "wti_future.pkl",
              'spsy.pkl', 'spny.pkl', 'spxhc.pkl', 'splrcd.pkl', 'splrci.pkl', 'splrcu.pkl', 'splrcs.pkl', 
              'splrct.pkl', 'splrcl.pkl', 'splrcm.pkl', 'ixbk.pkl', 'ixfn.pkl', 'ixid.pkl', 'ixis.pkl', 
              'ixk.pkl', 'ixtr.pkl', 'ixut.pkl', 'nbi.pkl', 'bkx.pkl' 
             ]
common_files_usa = [ "dji.pkl", "dji_future.pkl", "dxy_future.pkl", 
                  "ixic_future.pkl", "nas.pkl", "snp_future.pkl", "sox.pkl", "spx.pkl", 
                  "us_10yr_bond.pkl", "us_2yr_bond.pkl", "us_3mon_bond.pkl", "vix.pkl", "wti_future.pkl",
                  'spsy.pkl', 'spny.pkl', 'spxhc.pkl', 'splrcd.pkl', 'splrci.pkl', 'splrcu.pkl', 'splrcs.pkl', 
                  'splrct.pkl', 'splrcl.pkl', 'splrcm.pkl', 'ixbk.pkl', 'ixfn.pkl', 'ixid.pkl', 'ixis.pkl', 
                  'ixk.pkl', 'ixtr.pkl', 'ixut.pkl', 'nbi.pkl', 'bkx.pkl' 
             ]
common_files_kor = [ "kor_10yr_bond.pkl", "kor_2yr_bond.pkl", "kosdaq.pkl", "kospi.pkl", "krw_rate.pkl", 
             ]

common_files_column_name = {'dji.pkl':'dji', 'dji_future.pkl':'dji_f', 'dxy_future.pkl':'dxy', 
                   'ixic_future.pkl':'ixic_f', 'kor_10yr_bond.pkl':'bond_kor_10',
                   'kor_2yr_bond.pkl':'bond_kor_2', 'kosdaq.pkl':'kosdaq', 'kospi.pkl':'kospi',
                   'krw_rate.pkl':'krw', 'nas.pkl':'ixic', 'snp_future.pkl':'spx_f',
                   'sox.pkl':'sox', 'spx.pkl':'spx', 'us_10yr_bond.pkl':'bond_usa_10',
                   'us_2yr_bond.pkl':'bond_usa_2', 'us_3mon_bond.pkl':'bond_usa_3m',
                   'vix.pkl':'vix', 'wti_future.pkl':'wti',
                   'spsy.pkl':'spsy', 'spny.pkl':'spny', 'spxhc.pkl':'spxhc', 'splrcd.pkl':'splrcd', 
                   'splrci.pkl':'splrci', 'splrcu.pkl':'splrcu', 'splrcs.pkl':'splrcs', 
                   'splrct.pkl':'splrct', 'splrcl.pkl':'splrcl', 'splrcm.pkl':'splrcm', 
                   'ixbk.pkl':'ixbk', 'ixfn.pkl':'ixfn', 'ixid.pkl':'ixid', 'ixis.pkl':'ixis', 
                   'ixk.pkl':'ixk', 'ixtr.pkl':'ixtr', 'ixut.pkl':'ixut', 'nbi.pkl':'nbi', 'bkx.pkl':'bkx'
                   }


columns_investor_p1 = ['retail_1', 'foreigner_1', 'institution_1', 'financial_1', 'invtrust_1', 'pension_1', 
            'privequity_1',  'insurance_1', 'corporateetc_1', # bank_1, 'financeetc_1 제외
            'foreigneretc_1']
columns_investor_p2 = ['retail_2', 'foreigner_2', 'institution_2', 'financial_2', 'invtrust_2', 'pension_2',
            'privequity_2', 'insurance_2', 'corporateetc_2', # bank_2, 'financeetc_2 제외
            'foreigneretc_2']
columns_historical_p1 = ['open_1', 'high_1', 'low_1', 'close_1', 'vol_1']
columns_historical_p2 = ['open_2', 'high_2', 'low_2', 'close_2', 'vol_2']
columns_change_ratio = ['weekday', 'cr_00', 'cr_05', 'cr_10', 'cr_15', 'cr_20']
columns_common_p1 = ["dji_cr", "dji_f_cr", "dxy_cr", "ixic_f_cr", "bond_kor_10_cr", "bond_kor_2_cr", "kosdaq_cr", "kospi_cr", 
         "krw_cr", "ixic_cr", "spx_f_cr", "sox_cr", "spx_cr", "bond_usa_10_cr", "bond_usa_2_cr", "bond_usa_3m_cr", 
         "vix_cr", "wti_cr", "spsy_cr", "spny_cr", "spxhc_cr", "splrcd_cr", "splrci_cr", "splrcu_cr", "splrcs_cr",
         "splrct_cr", "splrcl_cr", "splrcm_cr", "ixbk_cr", "ixfn_cr", "ixid_cr", "ixis_cr", "ixk_cr", "ixtr_cr",
         "ixut_cr", "nbi_cr", "bkx_cr"]
columns_common_p2 = ["dji_cr_2", "dji_f_cr_2", "dxy_cr_2", "ixic_f_cr_2", "bond_kor_10_cr_2", "bond_kor_2_cr_2", "kosdaq_cr_2", "kospi_cr_2",
         "krw_cr_2", "ixic_cr_2", "spx_f_cr_2", "sox_cr_2", "spx_cr_2", "bond_usa_10_cr_2", "bond_usa_2_cr_2", "bond_usa_3m_cr_2",
         "vix_cr_2", "wti_cr_2", "spsy_cr_2", "spny_cr_2", "spxhc_cr_2", "splrcd_cr_2", "splrci_cr_2", "splrcu_cr_2",
         "splrcs_cr_2", "splrct_cr_2", "splrcl_cr_2", "splrcm_cr_2", "ixbk_cr_2", "ixfn_cr_2", "ixid_cr_2",
         "ixis_cr_2", "ixk_cr_2", "ixtr_cr_2", "ixut_cr_2", "nbi_cr_2", "bkx_cr_2"]
columns_futures_p1 = ['ixic_f_cr',   'spx_f_cr',   'dji_f_cr',
                      'wti_cr',   'dxy_cr',  'bond_usa_10_cr' ]  # 선물이 끝나는 시간이 명확하지 않아 제외 -1일 비교
columns_futures_p2 = ['ixic_f_cr_2', 'spx_f_cr_2', 'dji_f_cr_2',
                      'wti_cr_2', 'dxy_cr_2','bond_usa_10_cr_2' ] # 선물이 끝나는 시간이 명확하지 않아 제외 -2일 비교
columns_except = ['bank_1', 'financeetc_1', 'bank_2', 'financeetc_2'] # 자료가 많이 빠져 있어서 제외


col_inv1 = ['retail_1', 'foreigner_1', 'institution_1', 'financial_1', 'invtrust_1', 'pension_1', 'privequity_1', 
            'bank_1', 'insurance_1', 'financeetc_1', 'corporateetc_1', 'foreigneretc_1']

col_inv2 = ['retail_2', 'foreigner_2', 'institution_2', 'financial_2', 'invtrust_2', 'pension_2',
            'privequity_2', 'bank_2', 'insurance_2', 'financeetc_2', 'corporateetc_2', 'foreigneretc_2']
col_his1 = ['open_1', 'high_1', 'low_1', 'close_1', 'vol_1']
col_his2 = ['open_2', 'high_2', 'low_2', 'close_2', 'vol_2']
col_cr = ['weekday', 'cr_00', 'cr_05', 'cr_10', 'cr_15', 'cr_20']
col_common1 = ["dji_cr", "dji_f_cr", "dxy_cr", "ixic_f_cr", "bond_kor_10_cr", "bond_kor_2_cr", "kosdaq_cr", "kospi_cr", 
         "krw_cr", "ixic_cr", "spx_f_cr", "sox_cr", "spx_cr", "bond_usa_10_cr", "bond_usa_2_cr", "bond_usa_3m_cr", 
         "vix_cr", "wti_cr", "spsy_cr", "spny_cr", "spxhc_cr", "splrcd_cr", "splrci_cr", "splrcu_cr", "splrcs_cr",
         "splrct_cr", "splrcl_cr", "splrcm_cr", "ixbk_cr", "ixfn_cr", "ixid_cr", "ixis_cr", "ixk_cr", "ixtr_cr",
         "ixut_cr", "nbi_cr", "bkx_cr"]
col_common2 = ["dji_cr_2", "dji_f_cr_2", "dxy_cr_2", "ixic_f_cr_2", "bond_kor_10_cr_2", "bond_kor_2_cr_2", "kosdaq_cr_2", "kospi_cr_2",
         "krw_cr_2", "ixic_cr_2", "spx_f_cr_2", "sox_cr_2", "spx_cr_2", "bond_usa_10_cr_2", "bond_usa_2_cr_2", "bond_usa_3m_cr_2",
         "vix_cr_2", "wti_cr_2", "spsy_cr_2", "spny_cr_2", "spxhc_cr_2", "splrcd_cr_2", "splrci_cr_2", "splrcu_cr_2",
         "splrcs_cr_2", "splrct_cr_2", "splrcl_cr_2", "splrcm_cr_2", "ixbk_cr_2", "ixfn_cr_2", "ixid_cr_2",
         "ixis_cr_2", "ixk_cr_2", "ixtr_cr_2", "ixut_cr_2", "nbi_cr_2", "bkx_cr_2"]