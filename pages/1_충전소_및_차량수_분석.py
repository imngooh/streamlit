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
    initial_sidebar_state= 'expanded'
)
st.title('📌 충전기 수와 전기차 수 비교')

# 데이터 읽어오기
ee_per = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/ee_per.csv')
oil_cc = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/oil_cc.csv')
fuel_ee = pd.read_csv('https://raw.githubusercontent.com/imngooh/ais7_demo/main/fuel_ee.csv')



'## 🔌 충전기 당 전기차 수'
'자치구 별 충전기 하나당 담당하는 전기차 수'
st.bar_chart(data = ee_per, x='자치구', y='충전기 당 전기차')
with st.expander('데이터프레임으로 보기'):
    ee_per

"""
#### 📑 분석 결과
- 최소 : 9대(도봉구), 최대 : 96대(강남구)
- 자치구 구분 없이 본다면, 전기차 충전기 한 개당 전기차 26대 담당
- 완속충전기(하루에 6대 충전)만 생각하면, 완속충전기 한 개당 42대 담당
- 급속충전기(하루에 24대 충전)만 생각하면, 급속충전기 한 개당 70대 담당
- 급속충전기 : 완속충전기 = 평균 2 : 3 비율로 존재  
  
-> 단순 연산시, 충전기 하나당 하루에 13대의 전기차 충전 가능  
-> 서울시 전체 : 절대적으로 부족한 수치는 아님(이틀에 한 번 충전 가능)

그러나, 이는 서울시 전체를 평균내어 계산했을때의 수치로,  
자치구 별로 본다면 강남구, 은평구, 구로구, 금천구의 네 자치구는 충전기 하나당 전기차 수가 40대 이상으로, 3일에 한 번도 차량을 충전하지 못할 수 있는 부족한 상황이다.


#### 📣 결론
> 강남구, 은평구, 구로구, 금천구 등 일부 자치구의 경우 전기차의 수에 비해 충전기의 수가 부족하다.
"""


'## ⛽ 주유기 당 자동차 수와 비교'
'주유기 당 화석연료 자동차 수'
st.bar_chart(data = oil_cc, x='자치구', y='주유기 당 자동차')
with st.expander('주유기 당 자동차 수 데이터프레임으로 보기'):
    oil_cc

'주유기 당 자동차 수 및 충전기 당 전기차 수 비교'
st.image('https://s3.us-west-2.amazonaws.com/secure.notion-static.com/e15e63a9-7d29-4ab9-a11e-88d3516706c9/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221022%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221022T183450Z&X-Amz-Expires=86400&X-Amz-Signature=1cbbbd7d99da045ee1c558f443f7c3cf9e7bffd92d1a2d014951fea2ce457782&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject')
with st.expander('주유기 및 충전기 당 차량 수 비교 데이터프레임'):
    fuel_ee



"""

#### 🧮 분석 결과
- 주유기 한 개당 자동차가, 충전기 한 개당 전기차보다 평균 80배 많았다.
- 주유 시간 당 주행거리 비교
    - 화석연료 차량 : 4분 주유, 1000km 주행
    - 전기차량 : 4분 주유, 15km 주행
        - 급속(30분 충전), 완속(4시간 충전) : 220km 주행
        - 급속충전 빈도 : 완속충전 빈도 = 3 : 4
""" 
"""

- 주유 시간당 주행거리 비교 결과, 충전 횟수가 주유 횟수에 비해 66배 커야 한다.
- 즉, 충전기가 담당하는 자동차가 주유기가 담당하는 자동차의 1/66배 이하여야 한다.

-> 따라서, 단순 수치상으로 볼 때는 주유기의 개수에 비해 충전기의 개수는 부족하지 않다.

그러나, 주유소의 경우 1회 주유에 걸리는 시간이 짧아 주유가 가능한 시간대에 큰 제약이 있지 않은 반면, 전기차 충전소의 경우 1회 충전시 소요시간이 길어 충전이 가능한 시간대에 제약이 있다.
따라서 충전 가능한 시간대의 제약으로 인해 충전 가능한 횟수가 많이 줄어들 것이고, 충전소의 개수가 부족한 효과를 낼 것이라 예측할 수 있다.

#### 📣 결론
> 단순 수치상으로는 주유소에 비해 충전소가 부족하지 않다.
> 그러나 충전 시간이 오래걸려 충전 가능한 시간대에 제약이 있으므로 부족할 가능성이 높다.

"""
'## 📢 최종 비교'
"""
단순히 충전기의 개수, 전기차의 수만 놓고 보자면, 전기차 충전소의 부족은 존재하긴 하나 심각하지는 않다.

그러나, 주유소와의 비교에서 언급했듯이 충전에 오랜 시간이 걸려 아무때나 충전할 수 없고, 퇴근 후와 같이 여유 있는 시간대에만 충전할 수 있으므로 수치적으로 보았을 때보다 충전소의 부족 문제가 심각할 것이라 예상된다.

#### 👉 따라서, '시간대에 따른 충전 데이터'를 분석해 충전소가 실제로 부족한지 살펴본다.
"""
