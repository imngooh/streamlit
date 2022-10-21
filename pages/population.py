import numpy as np
import pandas as pd
import seaborn as sns
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import streamlit_folium
import streamlit as st




st.set_page_config(
    page_title="유동인구와 충전 데이터 비교",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state= 'expanded'
)

st.write('# 유동인구와 충전 데이터 비교 ')
st.sidebar.markdown('# 자치구 선택')


# 데이터 읽기

df_1 = pd.read_csv('https://raw.githubusercontent.com/cryptnomy/likelion-ai-s7-mid/master/data/hypo_1_pre.csv')

df_2 = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')

data_gu_time = df_1.iloc[:, [1, 4, 5]].groupby(['자치구', '시간대구분']).mean().reset_index()
data_gu_unique = data_gu_time['자치구'].unique()






# 선택지 만들기
selected_gu = st.sidebar.selectbox('name', list(df_1['자치구'].unique()))
if bool(selected_gu):
    selected_data = df_1[df_1['자치구'] == selected_gu]

st.markdown('## 상업 및 주거지역 비교 그래프')





# 그래프 그리기 위한 변수 처리
time_list = [x for x in range(24)]
df_2 = df_2.rename(columns = {str(x) : x for x in range(24)})

df_2.pivot_table(index = '자치구', values = time_list, aggfunc = 'sum')
gu_time = pd.DataFrame(df_2.pivot_table(index = '자치구', values = time_list, aggfunc = 'sum').stack())
gu_time = gu_time.reset_index().rename(columns = {'level_1' : '시간대'})
gu_time = gu_time.rename(columns={0:"충전빈도수"})

data_gu_time = data_gu_time.rename(columns = {'시간대구분' : '시간대'})
compare_time = pd.merge(data_gu_time, gu_time)
gu_list = compare_time['자치구'].unique().tolist()

gu_list = compare_time['자치구'].unique().tolist()




## 구현할 것:
# 거주지역과 산업지역 구분하여 리스트 만들고, 거주지 산업지 그래프 각각 그려주기

gu_not_home = ['강남구','금천구','마포구','서대문구','서초구','영등포구','성동구','용산구','종로구','중구']

gu_home = ['강동구', '강북구', '강서구', '관악구' ,'광진구', '구로구','노원구', '도봉구', '동대문구' ,'동작구', '성북구', '송파구', '양천구',  '은평구', '중랑구']
# print(len(gu_not_home), len(gu_home))   ## 10, 15



# 비교 그래프
fig, axes = plt.subplots(1,2, figsize = (8,3))
axes2 = axes.copy()

y11 = compare_time[compare_time['자치구'] == '서초구'][['시간대','충전빈도수']]['충전빈도수']
y12 = compare_time[compare_time['자치구'] == '서초구'][['시간대','20세 이상 생활인구수']]['20세 이상 생활인구수']

axes[0].set_xlabel('시간대')
axes[0].set_ylabel('충전빈도')
axes[0].bar(time_list, y11, color='r', label='충전빈도')
axes[0].legend(loc='lower right')
axes[0].set_title('상업지역')

axes2[0] = axes[0].twinx()

axes2[0].set_xlabel('시간대')
axes2[0].set_ylabel('생활인구수')
axes2[0].plot(time_list, y12, color='g', label='생활인구', linewidth = '5')
axes2[0].legend(loc='upper right')

y21 = compare_time[compare_time['자치구'] == '강서구'][['시간대','충전빈도수']]['충전빈도수']
y22 = compare_time[compare_time['자치구'] == '강서구'][['시간대','20세 이상 생활인구수']]['20세 이상 생활인구수']

axes[1].set_xlabel('시간대')
axes[1].set_ylabel('충전빈도')
axes[1].bar(time_list, y21, color='r', label='충전빈도')
axes[1].legend(loc='lower right')
axes[1].set_title('주거지역')

axes2[1] = axes[1].twinx()

axes2[1].set_xlabel('시간대')
axes2[1].set_ylabel('생활인구수')
axes2[1].plot(time_list, y22, color='g', label='생활인구', linewidth = '5')
axes2[1].legend(loc='upper right')

plt.tight_layout()
st.pyplot(fig)

st.markdown('## 선택 지역 확인하기')
# 선택한 구 그리고, 주거지역인지 상업지역인지 표시
fig3, axes = plt.subplots()
y1 = compare_time[compare_time['자치구'] == selected_gu][['시간대','충전빈도수']]['충전빈도수']
y2 = compare_time[compare_time['자치구'] == selected_gu][['시간대','20세 이상 생활인구수']]['20세 이상 생활인구수']

axes.set_xlabel('시간대')
axes.set_ylabel('충전빈도')
axes.bar(time_list, y1, color='r', label='충전빈도')
axes.legend(loc='lower right')
axes.set_title(selected_gu)

axes2 = axes.twinx()
axes2.set_xlabel('시간대')
axes2.set_ylabel('생활인구수')
axes2.plot(time_list, y2, color='g', label='생활인구', linewidth = '15')
axes2.legend(loc='upper right')
st.pyplot(fig3)

locat = '주거지역' if selected_gu in gu_home else '상업지역'
st.markdown(f'**{selected_gu}**는 **{locat}**입니다.')


### 실습 파일 내용

# st.markdown('## 그래프')

# pxhist = px.histogram(data, x='origin',title='지역별 연비 데이터 수')
# st.plotly_chart(pxhist)

# fig, axes = plt.subplots()
# sns.barplot(data = data, x='origin', y='mpg').set_title('지역별 자동차 연비')
# plt.tight_layout()
# st.pyplot(fig)

# st.line_chart(selected_data['mpg'])

# st.bar_chart(selected_data['mpg'])

# # 나만의 그래프 그려보기 그래 한번 그려보자 뭘 그려볼까
# st.bar_chart(data=data, x='name', y='mpg')

# fig2, axes = plt.subplots()
# sns.barplot(data = data, x='cylinders', y='mpg', hue = 'origin', ci=None).set_title('지역 및 기통 별 연비')
# st.pyplot(fig2)

# # 참 다양한 그래프가 있는데 왜 맨날 bar만 생각나는지 원! 그리고 집계!
# # raw data에 대한 그래프를 그리는 연습을 좀 해야한다. 분명히!

# fig3, axes = plt.subplots()
# sns.scatterplot(data = data, x='weight', y='mpg', hue = 'cylinders', palette = 'rainbow').set_title('mpg VS cylinders')
# st.pyplot(fig3)

# fig4, axes = plt.subplots()
# sns.violinplot(data=data, x='cylinders', y='mpg').set_title('mpg per cylinders')
# st.pyplot(fig4)

# ## 오 그냥 이렇게 해줘도 되나? 된다!!

# fig5 = sns.catplot(data= data, x='model_year', y='mpg', kind = 'box')
# plt.title('연식 별 연비')
# st.pyplot(fig5)