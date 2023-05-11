import os
import json
import streamlit as st
from utils import generate_self_evaluation, check_requirements

# 環境変数から等級要件を読み込む
grade_requirements_str = os.environ.get("GRADE_REQUIREMENTS")
grade_requirements = json.loads(grade_requirements_str)

st.title("自己評価ツール")

achievement_points = st.text_input("実績の要点を入力してください:")
grade = st.selectbox("目指す等級を選択してください:", [2, 3, 4])

if st.button("自己評価生成"):
    if check_requirements(achievement_points, grade):
        self_evaluation = generate_self_evaluation(achievement_points)
        st.success("等級要件を満たしています。")
        st.write(f"自己評価: {self_evaluation}")
    else:
        st.error("等級要件を満たしていません。要件を確認し、実績の要点を修正してください。")