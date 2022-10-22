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

# 2 전처리 데이터 읽어오기
df = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')

# 지도 표시
final_map = folium.Map(location = [37.5759,126.9768], zoom_start = 11)

# 지도 추가하기 위한 데이터
df_map = pd.DataFrame(df['충전소명'].unique()).rename(columns = {0 : '충전소명'})
df_map = pd.merge(df_map, df.groupby(['충전소명','위도','경도','급속충전기(대)','완속충전기(대)']).mean().reset_index()[['위도','경도','충전소명','급속충전기(대)','완속충전기(대)']], on ='충전소명')
df_map = pd.merge(df.groupby(['자치구','충전소명']).sum().reset_index()[['자치구','충전소명']], df_map)
df_gu_map= pd.merge(df_map.groupby('자치구')[['급속충전기(대)','완속충전기(대)']].sum().reset_index(), df_map.groupby('자치구')['충전소명'].count().reset_index())
gu_loc = """강남구 37.5172 127.0473
강동구 37.5301 127.1238
강북구 37.6398 127.0255
강서구 37.5510 126.8495
관악구 37.4781 126.9515
광진구 37.5384 127.0822
구로구 37.4955 126.8876
금천구 37.4519 126.9020
노원구 37.6543 127.0575
도봉구 37.6688 127.0471
동대문구 37.5742 127.0398
동작구 37.5124 126.9393
마포구 37.5634 126.9034
서대문구 37.5793 126.9365
서초구 37.4836 127.0327
성동구 37.5634 127.0369
성북구 37.5894 127.0167
송파구 37.5117 127.1059
양천구 37.5170 126.8666
영등포구 37.5263 126.8963
용산구 37.5323 126.9907
은평구 37.6015 126.9304
종로구 37.5735 126.9790
중구 37.5641 126.9979
중랑구 37.6063 127.0932"""
gu_df = pd.DataFrame(gu_loc.split('\n'))[0].str.split(expand = True)
gu_df.columns = ['자치구', '위도','경도']
df_gu_map = pd.merge(df_gu_map, gu_df)

# 지도에 구획 추가
geo_data = requests.get('https://raw.githubusercontent.com/cubensys/Korea_District/master/3_%EC%84%9C%EC%9A%B8%EC%8B%9C_%EC%9E%90%EC%B9%98%EA%B5%AC/%EC%84%9C%EC%9A%B8_%EC%9E%90%EC%B9%98%EA%B5%AC_%EA%B2%BD%EA%B3%84_2017.geojson').json()

folium.Choropleth(
    geo_data = geo_data,
    data = df_gu_map,
    columns = ('자치구', '충전소명'),
    key_on="feature.properties.SIG_KOR_NM",
    fill_color = 'Blues',
    legend_name = '충전소 수',
).add_to(final_map)


# 지도에 마커 추가
    
for i, row in df_map.iterrows():
    iframe = folium.IFrame('충전소명 : '+ row['충전소명'] + '<br>' +'급속충전기 : ' + str(row['급속충전기(대)']) + '<br>' + '완속충전기 : '+ str(row['완속충전기(대)']))
    popup = folium.Popup(iframe,min_width=200, max_width=300)
    
    folium.Circle([row['위도'],row['경도']],
                  radius = 100,
                  color = 'red',
                  fill_color = 'crimson',
                  popup = popup).add_to(final_map)

st.markdown('# 한국전력공사 전기차 충전소 위치(서울특별시)')    
st_map = st_folium(final_map, width = 1500)
st.markdown('> 자치구 별 색상이 진할수록 충전기의 수가 많습니다.')
# 차트 추가하려면 이런거 필요
# Popup().add_child(
#         folium.Vega(vis2, width=450, height=250)
#     )