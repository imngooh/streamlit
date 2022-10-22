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

"""# 메인 페이지

### 주제에 대한 설명

시각화 자료 + 주제
"""





# 페이지 설정
# st.set_page_config(
#     page_title="12걸지 마시조",
#     page_icon="💢",
#     layout="wide",
#     initial_sidebar_state= 'expanded'
# )

# 제목 markdown
st.markdown('# 💢12걸지마시조')
st.markdown('## *MID PROJECT*')
st.markdown('## ***전기차 충전소는 정말로 부족한가?***')


# 2 전처리 데이터 읽어오기
df = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')
