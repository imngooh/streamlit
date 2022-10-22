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
    page_title="12걸지 마시조",
    page_icon="💢",
    initial_sidebar_state= 'expanded'
)


st.markdown('# 💢12걸지마시조 - *MID PROJECT*')
st.markdown('## ***전기차 충전소는 정말로 부족한가?***')

df = pd.read_parquet('https://github.com/cryptnomy/likelion-ai-s7-mid/blob/master/data/hypo_2.parqeut.gzip?raw=true')

