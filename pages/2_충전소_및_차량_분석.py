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
"""
<어느 자치구 충전기가 부족한가?>

- 전기차 등록 대수 추이 / 타연료 자동차 등록 대슈 추이 비교

(새로 시각화 해야 함)

- 평균 주유기 대수 대비 이용 자동차 대수 vs 충전기 개수 대비 전기차 충전 빈도
"""



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


folium.Choropleth(
    geo_data = geo_data,
    data = ee_per,
    columns = ('자치구', '충전기 당 전기차'),
    key_on="feature.properties.SIG_KOR_NM",
    fill_color = 'Blues',
    legend_name = '충전소 수',
).add_to(final_map)


# 지도에 마커 추가
    
# for i, row in df_gu_map.iterrows():
#     iframe = folium.IFrame('자치구명 : '+ row['자치구'] + '<br>' +'급속충전기 : ' + str(row['급속충전기(대)']) + '<br>' + '완속충전기 : '+ str(row['완속충전기(대)']))
#     popup = folium.Popup(iframe,min_width=200, max_width=300)
    
#     folium.Circle([row['위도'],row['경도']],
#                   radius = 150,
#                   color = 'red',
#                   fill_color = 'crimson',
#                   popup = popup).add_to(final_map)
    
# 클러스터 마커
from folium.plugins import MarkerCluster
mc = MarkerCluster()

for i, row in df_map.iterrows():
    
    iframe = folium.IFrame('충전소명 : '+ row['충전소명'] + '<br>' +'급속충전기 : ' + str(row['급속충전기(대)']) + '<br>' + '완속충전기 : '+ str(row['완속충전기(대)']))
    popup = folium.Popup(iframe,min_width=200, max_width=300)
    
    mc.add_child(
        folium.Marker(location = [row['위도'], row['경도']],
               popup= popup
              )
    )

mc.add_to(final_map)    
    
    
    
st.markdown('# 한국전력공사 전기차 충전소 위치(서울특별시)')    
st_map = st_folium(final_map, width = 1500)
st.markdown('> 자치구 별 색상이 진할수록 충전기당 담당하는 전기차의 수가 많습니다.')

st.markdown('')
fig , ax= plt.subplots(figsize = (6,3))
sns.barplot(data=ee_per.sort_values("충전기 당 전기차", ascending= False), x="자치구", y="충전기 당 전기차", ci=None)

st.pyplot(fig)

# 지도에 차트 추가하려면 이런거 필요
# Popup().add_child(
#         folium.Vega(vis2, width=450, height=250)
#     )