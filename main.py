import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='cp949')  # euc-kr 또는 cp949
    return df

df = load_data()

# 데이터 확인
st.title("연령별 인구 현황 시각화")
st.write("원본 데이터 예시:")
st.dataframe(df.head())

# 컬럼 확인 및 전처리
st.subheader("데이터 전처리 및 시각화")

# 열 이름 보기
st.write("열 이름:")
st.write(df.columns.tolist())

# 성별 및 연령별로 인구 피라미드 그리기
if '행정기관' in df.columns and '연령(5세)' in df.columns and '총인구수 (명)' in df.columns:
    df_filtered = df[df['행정기관'] == '전국']  # 전국 데이터만 보기
    df_pivot = df_filtered.pivot_table(index='연령(5세)', columns='성별', values='총인구수 (명)', aggfunc='sum').fillna(0)

    # 남자는 음수로 변환해 인구 피라미드 형태 만들기
    df_pivot['남자'] *= -1

    # 인구 피라미드 그래프
    fig = px.bar(
        df_pivot,
        x=['남자', '여자'],
        y=df_pivot.index,
        orientation='h',
        title='성별 연령별 인구 피라미드 (전국)',
        labels={'value': '인구수', 'index': '연령대'},
        height=800
    )
    st.plotly_chart(fig)
else:
    st.error("필요한 열(예: '연령(5세)', '성별', '총인구수 (명)')이 데이터에 없습니다.")

