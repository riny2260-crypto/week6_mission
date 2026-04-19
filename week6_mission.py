import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 한글 폰트 설정 (절대 경로)
font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
font = fm.FontProperties(fname=font_path).get_name()

plt.rc('font', family=font)
plt.rcParams['axes.unicode_minus'] = False

st.write("폰트 로딩됨:", font)


# 2. 데이터 로드
try:
    df = pd.read_csv('6주차_실습4.csv', encoding='cp949')
    df.columns = df.columns.str.strip()

    st.sidebar.header("산점도 대상 컬럼 선택")

    cols = df.columns.tolist()
    x_axis = st.sidebar.selectbox("X축(설명 변수)", cols, index=cols.index('공부시간') if '공부시간' in cols else 0)
    y_axis = st.sidebar.selectbox("Y축(반응 변수)", cols, index=cols.index('점수') if '점수' in cols else 0)
    color_col = st.sidebar.selectbox(
        "색상으로 구분할 범주 컬럼 (선택)",
        [None] + cols,
        index=cols.index('전공') + 1 if '전공' in cols else 0
    )

    show_reg = st.sidebar.checkbox("추세선(회귀선) 표시", value=True)

    # 3. regplot으로 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    # 색상 구분이 있을 경우
    if color_col and color_col != "None":
        # 색상 구분된 산점도
        sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=color_col, ax=ax)

        # 추세선은 색상별로 각각 그릴 수 없으므로 전체 추세선 1개만 추가
        if show_reg:
            sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, ax=ax, color="black")
    else:
        # 색상 구분 없을 때
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        if show_reg:
            sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, ax=ax, color="red")

    ax.set_title(f"{x_axis}와(과) {y_axis}의 관계")

    st.pyplot(fig)

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. '6주차_실습4.csv' 파일이 같은 폴더에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

    import matplotlib
    import shutil

    font_dir = matplotlib.get_data_path() + '/fonts/ttf'
    shutil.copyfile('NanumGothic.ttf', font_dir + '/NanumGothic.ttf')
    fm._rebuild()
    plt.rc('font', family='NanumGothic')