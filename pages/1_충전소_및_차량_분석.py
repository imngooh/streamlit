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
st.title('충전기 수와 전기차 수 비교하기')


# 2 전처리 데이터 읽어오기
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


'## 충전기 당 전기차 수'

'## 주유기 당 자동차 수'

'## 충전 시간 및 주행거리 비교'


'## 최종 비교'

