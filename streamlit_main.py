import streamlit as st
import requests
from bs4 import BeautifulSoup
import json, pandas as pd

st.set_page_config (layout="wide")

# 매매/전세/월세 코드
tetradTpCd_options = {
    '전체': '',
    '매매': 'A1',
    '전세': 'B1',
    '월세': 'B2'
}
selected_tetradTpCd_name = st.selectbox('타입을 고르세요', list(tetradTpCd_options.keys()))
selected_tetradTpCd_value = tetradTpCd_options[selected_tetradTpCd_name]

# 단지 코드
hscpNo_options = {
    '옥수현대': '567',
    '브라운스톤남산': '14379',
    '신주에지앙': '105475'
}
selected_hscpNo_name = st.selectbox('단지를 고르세요', list(hscpNo_options.keys()))
selected_hscpNo_value = hscpNo_options[selected_hscpNo_name]



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
    return df
            

if st.button('데이터가져오기'):
    # 567    
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
    
    dfall = pd.DataFrame(columns=predefined_columns)
    print("초기값")
    print(dfall)
    
    
    temp_df = pd.DataFrame(get_APTInfo(selected_hscpNo_value, selected_tetradTpCd_value))
    print("처음부르기")
    print(temp_df)
    
    temp_df1 = temp_df.reindex(columns=predefined_columns)
    print("컬럼 조정 후")
    print(temp_df1)

    

    
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
    
    temp_df1 = temp_df1.set_axis(new_columns, axis=1)
    temp_df1.drop(rem_columns, axis=1, inplace=True)  
    print("display st")
    st.dataframe(temp_df1)  

    

    
    

    
    

