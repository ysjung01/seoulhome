import streamlit as st
import requests
from bs4 import BeautifulSoup
import json, pandas as pd

st.set_page_config (layout="wide")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

predefined_columns = [        
    'repImgUrl',
    'atclNo',
    'repImgTpCd',
    'vrfcTpCd',
    'atclNm',
    'bildNm',
    'tradTpCd',
    'tradTpNm',
    'rletTpCd',
    'rletTpNm',
    'spc1',	
    'spc2',	
    'flrInfo',	
    'atclFetrDesc',	
    'cfmYmd',	
    'prcInfo',	
    'sameAddrCnt',
    'sameAddrDirectCnt',
    'sameAddrHash',
    'sameAddrMaxPrc',	
    'sameAddrMinPrc',	
    'tradCmplYn',
    'tagList',
    'atclStatCd',
    'cpid',	
    'cpNm',	
    'cpCnt',	
    'cpLinkVO',	
    'rltrNm',	
    'directTradYn',	
    'direction',	
    'tradePriceHan',
    'tradeRentPrice',	
    'tradePriceInfo',	
    'tradeCheckedByOwner',
    'point',
    'dtlAddr',
    'dtlAddrYn',	
    'repImgThumb'
]

new_columns = [
    'repImgUrl',
    'atclNo',
    'repImgTpCd',
    'vrfcTpCd',
    '단지명',
    '동수',
    'tradTpCd',
    '거래타입',
    'rletTpCd',
    '건물유형',
    '공급면적',	
    '전용면적',	
    '층수',	
    '설명',	
    '등록일',	
    '매도가',	
    'sameAddrCnt',
    'sameAddrDirectCnt',
    'sameAddrHash',
    '매도가(MAX)',	
    '매도가(Min)',	
    'tradCmplYn',
    'tagList',
    'atclStatCd',
    'cpid',	
    'cpNm',	
    'cpCnt',	
    'cpLinkVO',	
    'rltrNm',	
    'directTradYn',	
    '방향',	
    'tradePriceHan',
    'tradeRentPrice',	
    'tradePriceInfo',	
    'tradeCheckedByOwner',
    'point',
    'dtlAddr',
    'dtlAddrYn',	
    'repImgThumb'
]

rem_columns = [
    'repImgUrl',
    'atclNo',
    'repImgTpCd',
    'vrfcTpCd',
    'tradTpCd',
    'rletTpCd',
    'sameAddrCnt',
    'sameAddrDirectCnt',
    'sameAddrHash',
    '매도가(MAX)',	
    '매도가(Min)',	
    'tradCmplYn',
    'tagList',
    'atclStatCd',
    'cpid',	
    'cpNm',	
    'cpCnt',	
    'cpLinkVO',	
    'rltrNm',	
    'directTradYn',	
    'tradePriceHan',
    'tradeRentPrice',	
    'tradePriceInfo',	
    'tradeCheckedByOwner',
    'point',
    'dtlAddr',
    'dtlAddrYn',	
    'repImgThumb'
]
    


# get_APIinfo(search_apt):  
# input : 아파트명
# output : 검색된 아파트 정보 Dataframe
def get_APIsnum(search_apt):        

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    remaked_URL = "https://new.land.naver.com/api/search?keyword={}&page=1".format(search_apt)

    res = requests.get(remaked_URL, headers=headers)
    json_str = json.loads(json.dumps(res.json()))
    
    APTlist = json_str['complexes'] 

    df = pd.DataFrame(APTlist)

    res_df = pd.DataFrame(columns=['complexName', 'complexNo', 'cortarAddress'])

    res_df['complexName'] = df['complexName']
    res_df['complexNo'] = df['complexNo']
    res_df['cortarAddress'] = df['cortarAddress']

    return res_df

# get_APTInfo(hscpNo, tetradTpCd)::  
# input : hscpNo : 아파트번호, tetradTpCd : 거래타입
# output : 검색된 아파트 정보 Dataframe
def get_APTInfo(hscpNo, tetradTpCd):
    req_URL = "https://m.land.naver.com/complex/getComplexArticleList"
    param = {
        'hscpNo': hscpNo,
        'tradTpCd': tetradTpCd,
        'order': 'point',
        'showR0': 'N',
        'page': '1',

    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }


    resp = requests.post(req_URL, params=param, headers=header)
    json_str = json.loads(json.dumps(resp.json()))

    APTlist = json_str['result']['list']
    df = pd.DataFrame(APTlist)

    page = 1
    while True:
        page += 1
        param['page'] = page

        resp = requests.post(req_URL, params=param, headers=header)
        json_str = json.loads(json.dumps(resp.json()))


        if len(json_str['result']['list']) == 0:
            break

        APTlist = json_str['result']['list']
        nex_df = pd.DataFrame(APTlist)
        df = pd.concat([df,nex_df])
    
    if df.empty == False :
        df['flrInfo'] = df['flrInfo'].str.replace('/', ' // ')
    
    
    return df

# 초기화: 세션 상태
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = pd.DataFrame()
if 'selected_hscpNo_value' not in st.session_state:
    st.session_state['selected_hscpNo_name'] = None
if 'selected_hscpNo_value' not in st.session_state:
    st.session_state['selected_hscpNo_value'] = None
if 'df_apts_sinfo' not in st.session_state:
    st.session_state['df_apts_sinfo'] = pd.DataFrame()
    

# 아파트 번호 정보를 출력하기 위한 df 
df_apts_sinfo = pd.DataFrame(columns=['complexName', 'complexNo', 'cortarAddress'])


# 1단계: 아파트이름으로 아파트리스트 검색
search_apt = st.text_input('아파트 이름을 검색하세요:') 
search_button = st.button('검색')

if search_button:
    st.session_state['search_results'] = pd.DataFrame(get_APIsnum(search_apt)) 
    st.session_state['selected_hscpNo_name'] = None
    st.session_state['selected_hscpNo_value'] = None


# 2단계 : 아파트 단지 리스트 표기 및 선택
if not st.session_state['search_results'].empty:
    st.write(st.session_state['search_results'])
    APT_name = st.selectbox('아파트를 선택하세요:', st.session_state['search_results']['complexName'])
    if APT_name:
        selected_APT = st.session_state['search_results'][st.session_state['search_results']['complexName'] == APT_name]
        st.session_state['selected_hscpNo_name'] = selected_APT['complexName'].values[0]
        st.session_state['selected_hscpNo_value'] = selected_APT['complexNo'].values[0]    

# 2단계: 거래 타입 설정
if st.session_state['selected_hscpNo_value'] :
    # 매매/전세/월세 코드
    tetradTpCd_options = {
        '전체': '',
        '매매': 'A1',
        '전세': 'B1',
        '월세': 'B2'
    }
    selected_tetradTpCd_name = st.selectbox('타입을 고르세요', list(tetradTpCd_options.keys()))
    st.session_state['selected_tetradTpCd_value']  = tetradTpCd_options[selected_tetradTpCd_name]   


if st.session_state['selected_hscpNo_value'] :     
    if st.button('데이터가져오기'):
        dfall = pd.DataFrame(columns=predefined_columns)
        

        temp_df = pd.DataFrame(get_APTInfo(st.session_state['selected_hscpNo_value'], st.session_state['selected_tetradTpCd_value']))
        
        temp_df1 = temp_df.reindex(columns=predefined_columns)

        
        temp_df1 = temp_df1.set_axis(new_columns, axis=1)
        temp_df1.drop(rem_columns, axis=1, inplace=True)  

        st.dataframe(temp_df1) 
