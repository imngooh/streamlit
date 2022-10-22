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




# st.set_page_config(
#     page_title="유동인구와 충전 데이터 비교",
#     page_icon="👨‍👩‍👧‍👦",
#     layout="wide",
#     initial_sidebar_state= 'expanded'
# )


"""
<보통 어느 시간대에 무슨 충전기로 충전하나?>

- 전체 자치구의 시간대별 충전 수
- 전체 자치구의 시간대별 충전수 (급속/완속) -> 양상이 아예 다르다

<자치구별로 어떤 유동인구 특성에 따른 시간대 이용 차이가 있는가?>

- 주거지역/근무지역 나눠서 subplot 유동인구/충전빈도 이중축 그래프
"""



st.write('# 시간대별 충전 빈도수를 통한 충전소 부족여부 파악 ')
st.sidebar.markdown('# 자치구 선택')


# 데이터 읽기

df_1 = pd.read_csv('https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/hypo_1_pre.csv')
df_2 = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')

# 데이터 프레임 처리
time_list = [x for x in range(24)]
df_2 = df_2.rename(columns = {str(x) : x for x in range(24)})


# 전체 자치구 시간대별 충전 수
time_count = pd.DataFrame(df_2[time_list].sum()).reset_index().rename(columns = {'index' : '시간대', 0 : '충전수'})
# 시각화
fig0 = plt.figure(figsize = (8,4))
sns.barplot(data = time_count, x='시간대', y='충전수', ci = None, estimator = sum)
plt.ylabel('충전수')
plt.title('시간대별 충전수')
st.pyplot(fig0)

# 완속 급속 충전수

fig1, ax = plt.subplots()

plt.bar(time_list,df_2.groupby('충전구분')[time_list].sum().T.reset_index()['완속'],width = 0.2, label = '완속')
plt.bar(np.array(time_list) +0.2,df_2.groupby('충전구분')[time_list].sum().T.reset_index()['급속'],width = 0.2,label = '급속')

plt.title('시간대별 완속, 급속 충전수 비교')
plt.legend(loc ='best')
st.pyplot(fig1)


# 선택지 만들기
selected_gu = st.sidebar.selectbox('name', list(df_1['자치구'].unique()))
if bool(selected_gu):
    selected_data = df_1[df_1['자치구'] == selected_gu]






# 그래프 그리기 위한 변수 처리


data_gu_time = df_1.iloc[:, [1, 4, 5]].groupby(['자치구', '시간대구분']).mean().reset_index()
data_gu_time = data_gu_time.rename(columns = {'시간대구분' : '시간대'})

data_gu_unique = data_gu_time['자치구'].unique()

gu_time = pd.DataFrame(df_2.pivot_table(index = '자치구', values = time_list, aggfunc = 'sum').stack())
gu_time = gu_time.reset_index().rename(columns = {'level_1' : '시간대'})
gu_time = gu_time.rename(columns={0:"충전빈도수"})
compare_time = pd.merge(data_gu_time, gu_time)
gu_list = compare_time['자치구'].unique().tolist()
selected_gu_time = compare_time[compare_time['자치구'] == selected_gu].set_index('시간대')


## 구현할 것:
# 거주지역과 산업지역 구분하여 리스트 만들고, 거주지 산업지 그래프 각각 그려주기

gu_not_home = ['강남구','금천구','마포구','서대문구','서초구','영등포구','성동구','용산구','종로구','중구']
gu_home = ['강동구', '강북구', '강서구', '관악구' ,'광진구', '구로구','노원구', '도봉구', '동대문구' ,'동작구', '성북구', '송파구', '양천구',  '은평구', '중랑구']


st.write('# 유동인구와 충전 빈도수 비교')
st.markdown('## 상업 및 주거지역 비교')

# 비교 그래프
plt.style.use('seaborn-paper')
print(plt.style.available)
fig, axes = plt.subplots(1,2, figsize = (8,3))
axes2 = axes.copy()

y11 = compare_time[compare_time['자치구'] == '서초구'][['시간대','충전빈도수']]['충전빈도수']
y12 = compare_time[compare_time['자치구'] == '서초구'][['시간대','20세 이상 생활인구수']]['20세 이상 생활인구수']

axes[0].set_xlabel('시간대')
axes[0].bar(time_list, y11, color = '#FF8B8B',label='충전빈도')
axes[0].legend(loc='best')
axes[0].set_title('상업지역')


axes2[0] = axes[0].twinx()
axes2[0].plot(time_list, y12, color = '#167C80',label='생활인구', linewidth = '5')
axes2[0].legend(loc='lower left')
plt.gca().axes.yaxis.set_visible(False)

y21 = compare_time[compare_time['자치구'] == '성북구'][['시간대','충전빈도수']]['충전빈도수']
y22 = compare_time[compare_time['자치구'] == '성북구'][['시간대','20세 이상 생활인구수']]['20세 이상 생활인구수']


axes[1].bar(time_list, y21, color = '#FF8B8B',label='충전빈도')
axes[1].legend(loc='lower right')
axes[1].set_title('주거지역')
axes[1].set_xlabel('시간대')


axes2[1] = axes[1].twinx()

axes2[1].plot(time_list, y22, color = '#167C80',label='생활인구', linewidth = '5')
axes2[1].legend(loc='lower left')
plt.gca().axes.yaxis.set_visible(False)

plt.tight_layout()
st.pyplot(fig)

# 상업지역 및 주거지역 비교
st.markdown('#### 상업지역')
st.markdown('**오전 및 오후** 시간대에 생활인구 **많음**, **야간** 시간대에 **없음**')

st.markdown('#### 주거지역')
st.markdown('**오전 및 오후** 시간대에 생활인구 **적음**, **야간** 시간대에 **많음**')




st.markdown('')
st.markdown('### 선택한 지역 그래프 확인하기')
st.markdown('> 왼쪽 사이드바에서 자치구를 선택하세요!')

# 선택한 구 그리고, 주거지역인지 상업지역인지 표시
# plotly 도전
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=1, shared_xaxes=True,specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=selected_gu_time.reset_index()['시간대'],y=selected_gu_time.reset_index()['충전빈도수'],
              name='충전수'))
fig.add_trace(go.Scatter(x=selected_gu_time.reset_index()['시간대'],y=selected_gu_time.reset_index()['20세 이상 생활인구수'],
              name='유동인구수'),secondary_y = True)

fig.update_layout(
    title_text= f"<b>{selected_gu}<b> 시간대별 충전 빈도수 및 유동인구 수"
)

fig.update_xaxes(title_text="시간대")
fig.update_yaxes(title_text="<b>충전 수</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>생활인구 수</b>", secondary_y=True)


st.plotly_chart(fig)

locat = '주거지역' if selected_gu in gu_home else '상업지역'
st.markdown(f'**{selected_gu}**는 **{locat}**입니다.')
if locat =='주거지역' :
    st.markdown('**오전 및 오후** 시간대에 생활인구가 **적고**, **야간** 시간대에 **많습니다.**')
else :
    st.markdown('**오전 및 오후** 시간대에 생활인구가 **많고**, **야간** 시간대에 **적습니다.**')