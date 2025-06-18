import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로드
@st.cache_data
def load_data():
    # 적절한 인코딩 및 구분자 자동 감지 시도
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='cp949', skiprows=1)
    return df

df = load_data()

# 데이터 구조 확인
if df.shape[1] < 3:
    st.error("CSV 파일 형식이 예상과 다릅니다. 열 구조를 확인해주세요.")
    st.stop()

# 열 이름 할당 (수동 지정 필요할 수 있음)
df = df.rename(columns={df.columns[0]: "지역", df.columns[1]: "연령대", df.columns[2]: "총인구수"})

# 문자열 숫자 처리
df['총인구수'] = df['총인구수'].astype(str).str.replace(',', '', regex=False)
df['총인구수'] = pd.to_numeric(df['총인구수'], errors='coerce')

# 결측치 제거
df = df.dropna(subset=['총인구수'])

# Streamlit UI
st.title("📊 지역별 연령 인구 구조 시각화")
st.markdown("원하는 지역을 선택하면 해당 지역의 연령대별 인구 구조를 볼 수 있습니다.")

지역들 = df["지역"].unique()
selected_region = st.selectbox("지역 선택", 지역들)

# 선택한 지역 필터링
filtered_df = df[df["지역"] == selected_region]

# 시각화
fig = px.bar(
    filtered_df,
    x="총인구수",
    y="연령대",
    orientation='h',
    title=f"{selected_region}의 연령대별 인구 분포",
    labels={"총인구수": "인구 수", "연령대": "연령대"},
    height=600
)

st.plotly_chart(fig, use_container_width=True)
