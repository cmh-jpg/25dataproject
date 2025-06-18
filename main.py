import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="cp949", skiprows=3)
    df = df.dropna(how='all', axis=1)  # 전부 NaN인 열 제거
    df = df.rename(columns={df.columns[0]: "행정구역"})
    df["행정구역"] = df["행정구역"].str.strip()
    df = df[df["행정구역"].str.contains("합계") == False]  # "합계" 행 제거
    df = df.reset_index(drop=True)
    return df

# 데이터 로드
df = load_data()

# UI: 지역 선택
regions = df["행정구역"].unique()
selected_region = st.selectbox("📍 지역을 선택하세요:", regions)

# UI: 인구 유형 선택
pop_type = st.radio("👥 인구 유형을 선택하세요:", ["계", "남자", "여자"])

# 해당 지역 데이터 필터링
row = df[df["행정구역"] == selected_region].iloc[0]

# 열 이름에서 연령대 추출
age_columns = [col for col in df.columns if "세" in col and pop_type in col]
ages = [col.split("_")[0] for col in age_columns]
values = [int(str(row[col]).replace(",", "")) for col in age_columns]

# 시각화
fig = px.bar(
    x=values,
    y=ages,
    orientation="h",
    labels={"x": "인구 수", "y": "연령대"},
    title=f"{selected_region} - 연령대별 인구 ({pop_type})"
)
fig.update_layout(yaxis=dict(categoryorder='category ascending'))

# 출력
st.plotly_chart(fig, use_container_width=True)
