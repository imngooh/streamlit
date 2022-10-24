import numpy as np
import pandas as pd
import seaborn as sns
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import streamlit as st
import requests

# 페이지 설정
st.set_page_config(
    page_title="12걸지 마시조",
    page_icon="💢",
    initial_sidebar_state= 'expanded'
)

# 데이터 로드
df_gu_map = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/df_gu_map.csv')
df_map = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/df_map.csv')
ee_per = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/ee_per.csv')


# 지도 생성
final_map = folium.Map(location = [37.5759,126.9768], zoom_start = 11)

geo_data = requests.get('https://raw.githubusercontent.com/cubensys/Korea_District/master/3_%EC%84%9C%EC%9A%B8%EC%8B%9C_%EC%9E%90%EC%B9%98%EA%B5%AC/%EC%84%9C%EC%9A%B8_%EC%9E%90%EC%B9%98%EA%B5%AC_%EA%B2%BD%EA%B3%84_2017.geojson').json()

folium.Choropleth(
    geo_data = geo_data,
    data = ee_per,
    columns = ('자치구', '충전기 당 전기차'),
    key_on="feature.properties.SIG_KOR_NM",
    fill_color = 'Blues',
    legend_name = '충전소 수',
).add_to(final_map)
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



st.header("""💢12(시비)걸지마시조  
***MID project***  
멋쟁이 사자처럼 AI SCHOOL 7기  
김지현, 박경택, 이예원, 임종우, 정의민""")
# button = st.button('시작!')
# if bool(button) : st.balloons()
'---'
st.title('**📌전기차 충전소는 정말 부족한가?**')

st.image('https://img.freepik.com/premium-vector/electric-car-charging-its-battery-concept-illustration-for-green-environment_113065-28.jpg?w=1380')

'### 📈커지는 전기차 시장'
"""
- 전기차 판매량은 해마다 늘어나는 추세
- 2021년에는 신규 등록이 10만대를 돌파
"""
'### ⚡가장 큰 우려 : 충전소 부족'
"""
- 전기차를 구매하는데에 다양한 우려와 고민도 존재
- 가격, 안전성, 짧은 주행거리 등 다양한 원인
- 가장 큰 우려는 '충전소 부족'
    """
st.image('https://s3.us-west-2.amazonaws.com/secure.notion-static.com/b2343bc0-d564-4161-b61f-64e5a209a241/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221023%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221023T125335Z&X-Amz-Expires=86400&X-Amz-Signature=c2449abe1c15492cac43eec5b3ba624677dc029d1fa430b5eb50121ba750a5b5&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject')

'### 💭충전소는 진짜로 부족할까?'
with st.expander('🗺️서울특별시 내 충전기 지도로 살펴보기!') :
    st_map = folium_static(final_map)
    '배경 색상은 충전기 하나 당 담당하는 전기차 수를 의미합니다.'
st.image('https://github.com/imngooh/mid_1_folium/raw/main/%EC%A3%BC%EC%9C%A0%EC%86%8C%EC%B6%A9%EC%A0%84%EC%86%8C.png')
"""
- 서울특별시 자치구 별, 주유기 당 자동차 개수와 충전기 당 전기차 개수 비교 결과
- 주유기 한 개가 담당하는 자동차의 개수 충전기가 담당하는 전기차보다 월등히 많다.
- 그렇다면 전기차 충전기는 정말로 부족한 것일까? 단지 우려는 아닐까?


#### 👉 정말 부족한지 알아보고, 부족하면 해결 방법을 고안하자.

"""
'---'
'### 📊 알아본 방법 1. 충전기 수와 전기차 수 비교'
"""
- 충전기 개수 당 전기차 수 파악, 부족여부 확인
- 주유기 개수 당 전기차 수 파악
- 화석연료 차와, 전기차의 충전 소요시간 및 1회 충전시 주행거리 파악
- 비교하여 전기차 충전기가 진짜 부족한 것인지 파악


"""


'### 🕑 알아본 방법 2. 시간대별 분석을 통한 상대적 파악'
"""
- 시간대 별 충전 빈도수 파악
- 시간대 별 자치구 유동인구 파악
- 유동인구와 비교하여 분석
- 어느 지역에서, 어느 시간대에 부족한지 파악
- 충전이 주로 일어나는 시간대를 파악, 충전소의 수용량 및 1회 충전시 소요 시간과 비교

"""
'---'

'### 📢 결론 : 전기차 충전소는 부족하다.'
"""
절대적인 개수로 보아도 전기차 충전소는 부족하다. 그러나 그렇게 심각한 정도는 아니다.

그러나, 긴 충전시간으로 인한 충전 가능 시간대의 제약(오전 및 오후 일과 시간 내 불가능)이 존재하고, 이로 인해 야간 시간대의 충전 집중 현상이 일어난다. 그런데 야간충전의 대부분은 충전에 시간이 오래 걸리는 완속충전기로 진행된다. 따라서 야간충전에서 많은 차를 충전하기 힘들다. 이러한 이유로 인해, 절대적인 수치에 비해 사용자들이 체감하는 실제 충전기 부족 문제는 더 심각함을 알 수 있었다.
"""

'#### 📍 제언'
"""
충전기 부족 문제의 가장 큰 원인이 충전 가능 시간대의 제약과 완속 충전기의 많은 사용이었다.
따라서, 충전 가능 시간대에 제약이 없도록 유동인구가 많은 상업 지역에 급속 충전기를 추가로 설치하고, 다른 곳에도 급속 충전기의 보급을 늘린다면, 충전기 부족 문제를 효율적으로 줄일 수 있을 것이다.
"""

"""
---
[이미지1 출처](https://kr.freepik.com/premium-vector/electric-car-charging-its-battery-concept-illustration-for-green-environment_4868013.htm)

[이미지2 출처](https://daily.hankooki.com/news/articleView.html?idxno=496925)


"""