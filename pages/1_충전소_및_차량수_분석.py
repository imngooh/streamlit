import numpy as np
import pandas as pd
import seaborn as sns
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium
import streamlit as st
import requests

# 페이지 설정
st.set_page_config(
    page_title="충전소와 전기차 간 비교",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state= 'expanded'
)
st.title('충전기 수와 전기차 수 비교')


# 데이터 읽어오기
df = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')


ee_car = pd.read_csv('https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/seoul-any-gu-ev.csv', encoding = 'cp949')
ee_car['시군구별'] = ee_car['시군구별'].str.replace('중 구', '중구')
ee_car = ee_car[ee_car['연월별'] == '2021-12-31'][['시군구별','계']]
ee_car_mount = pd.DataFrame(ee_car.groupby('시군구별')['계'].sum()).reset_index()
ee_car_mount = ee_car_mount.rename(columns = {'시군구별' : '자치구'})
ee_station = df.groupby('자치구')['충전소명'].nunique().copy()
ee_station = pd.DataFrame(ee_station).reset_index()
ee_station = ee_station.rename(columns = {'충전소명' : '충전소수'})
ee_per = pd.merge(ee_car_mount,ee_station,on='자치구')
ee_per = ee_per.rename(columns = {"계" : "자치구별 전기차 대수"})
gu_charger = df.groupby(['자치구','충전소명'])[['급속충전기(대)','완속충전기(대)']].mean().groupby('자치구').sum().reset_index()
gu_charger['총 충전기수'] = gu_charger['급속충전기(대)'] + gu_charger['완속충전기(대)']
ee_per = pd.merge(ee_per , gu_charger)
ee_per['충전기 당 전기차'] = ee_per['자치구별 전기차 대수'] / ee_per['총 충전기수']


oil = pd.read_csv('https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/20221020101743.csv')
oil = oil[~oil['자치구별(2)'].str.contains('소계')]
oil = oil[oil['판매소별(2)'].str.startswith('주유소')]
oil = oil.drop(["자치구별(1)", "판매소별(1)", "2011","2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"], axis=1)
oil = oil.rename(columns = {"자치구별(2)" : "자치구", "판매소별(2)" : "판매소 유형", "2021" : "2021주유소 현황"})
oil_machine = pd.read_csv('https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C_%EC%84%B1%EB%B6%81%EA%B5%AC_%EC%A3%BC%EC%9C%A0%EC%86%8C_%ED%98%84%ED%99%A9_20210101.csv', encoding = 'cp949')
mean_oil = oil_machine['주유기수'].mean()
oil['주유기수'] = oil['2021주유소 현황'].astype(int).map(lambda x : round(x * mean_oil))


cc=pd.read_csv("https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/20221020162020.csv")
cc = cc[~cc['자치구별(2)'].str.startswith("소계")]
cc = cc[~cc['자치구별(2)'].str.startswith("자치구별(2)")]
cc = cc.drop(["자치구별(1)", "2021.1", "2021.2" , "2021.3" , "2021.4", "2021.5", "2021.6", "2021.7", "2021.8", "2021.9", "2021.10", "2021.11", "2021.12", "2021.13", "2021.14", "2021.15", "2021.16", "2021.17", "2021.18", "2021.19", "2021.20", "2021.21", "2021.22", "2021.23"], axis=1)
cc = cc.rename(columns = {"자치구별(2)" : "자치구", "2021" : "2021등록된자동차"})
oil_cc = pd.merge(oil,cc, how="left")
oil_cc["주유기 당 자동차"] = oil_cc["2021등록된자동차"].astype(int)/oil_cc["주유기수"]
oil_cc["주유기 당 자동차"] = round(oil_cc["주유기 당 자동차"], 2)


fuel_ee = pd.merge(oil_cc[['자치구','주유기 당 자동차']], ee_per[['자치구','충전기 당 전기차']], on ='자치구')







'## 충전기 당 전기차 수'
'자치구 별 충전기 하나당 담당하는 전기차 수'
st.bar_chart(data = ee_per, x='자치구', y='충전기 당 전기차')
with st.expander('데이터프레임으로 보기'):
    ee_per

"""
#### 분석 결과
- 최소 : 9대(도봉구), 최대 : 96대(강남구)
- 자치구 구분 없이 본다면, 전기차 충전기 한 개당 전기차 26대 담당
- 완속충전기만 생각하면, 완속충전기 한 개당 42대 담당
- 급속충전기만 생각하면, 급속충전기 한 개당 70대 담당

완속충전기 평균 80% 충전시간 : 4시간 -> 하루에 6대 충전 가능  
급속충전기 평균 80% 충전시간 : 30분 -> 하루에 24대 충전 가능  
급속충전기 : 완속충전기 = 평균 2 : 3 비율로 존재  
  
-> 단순 연산시, 충전기 하나당 하루에 13대의 전기차 충전 가능  
-> 서울시 전체 : 절대적으로 부족한 수치는 아님(이틀에 한 번 충전 가능)

그러나, 이는 서울시 전체를 평균내어 계산했을때의 수치로,  
자치구 별로 본다면 강남구, 은평구, 구로구, 금천구의 네 자치구는 충전기 하나당 전기차 수가 40 이상으로, 3일에 한 번도 차량을 충전하지 못할 수 있는 부족한 상황이다.

#### 결론
> 강남구 등 일부 자치구의 경우 부족하다.
"""


'## 주유기 당 자동차 수와 비교'
st.bar_chart(data = oil_cc, x='자치구', y='주유기 당 자동차')
with st.expander('데이터프레임으로 보기'):
    oil_cc
"""

#### 분석 결과
- 
- 
- 
- 

"""

'## 충전 시간 및 주행거리 비교'
fuel_ee

'## 최종 비교'
'부족하다'
