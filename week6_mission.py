import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 프로젝트에 포함된 NanumGothic 폰트 등록
font_path = "NanumGothic.ttf"  # 같은 폴더에 있으므로 파일명만 지정
font = fm.FontProperties(fname=font_path).get_name()
st.write("폰트 로딩됨:", font)

plt.rc('font', family=font)
plt.rcParams['axes.unicode_minus'] = False


# 1. 데이터 로드 (ANSI/CP949 인코딩 적용)
try:
    df = pd.read_csv('6주차_실습4.csv', encoding='cp949')
    # 컬럼명 공백 제거
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
        # lmplot은 ax 인자를 받지 않으므로 아래와 같이 작성합니다.
        g = sns.lmplot(data=df, x=x_axis, y=y_axis, hue=color_col, aspect=1.5)
        plt.title(f"{x_axis}와(과) {y_axis}의 관계")
        # g.fig는 lmplot이 생성한 Figure 객체입니다.
        st.pyplot(g.fig)
    else:
        # 일반 산점도는 ax를 사용할 수 있습니다.
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=color_col, ax=ax)
        plt.title(f"{x_axis}와(과) {y_axis}의 관계")
        st.pyplot(fig)

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. '6주차_실습4.csv' 파일이 같은 폴더에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")