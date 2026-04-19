import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 👈 로컬에서 한글을 자동으로 잡아주던 라이브러리

# 1. 데이터 로드 (ANSI/CP949 인코딩 적용)
try:
    df = pd.read_csv('6주차_실습4.csv', encoding='cp949')
    # 컬럼명 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    st.sidebar.header("산점도 대상 컬럼 선택")

    cols = df.columns.tolist()
    x_axis = st.sidebar.selectbox("X축(설명 변수)", cols, index=cols.index('공부시간') if '공부시간' in cols else 0)
    y_axis = st.sidebar.selectbox("Y축(반응 변수)", cols, index=cols.index('점수') if '점수' in cols else 0)
    color_col = st.sidebar.selectbox("색상으로 구분할 범주 컬럼 (선택)", [None] + cols,
                                     index=cols.index('전공') + 1 if '전공' in cols else 0)

    show_reg = st.sidebar.checkbox("추세선(회귀선) 표시", value=True)

    # 2. 그래프 그리기
    if show_reg:
        # lmplot으로 추세선이 포함된 산점도 그리기
        g = sns.lmplot(data=df, x=x_axis, y=y_axis, hue=color_col, aspect=1.5)
        plt.title(f"{x_axis}와(과) {y_axis}의 관계")
        # 최신 버전에서는 g.fig 대신 g.figure를 사용합니다.
        st.pyplot(g.figure)
    else:
        # 일반 산점도 그리기
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=color_col, ax=ax)
        plt.title(f"{x_axis}와(과) {y_axis}의 관계")
        st.pyplot(fig)

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. '6주차_실습4.csv' 파일이 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")