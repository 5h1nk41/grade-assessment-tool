import os
import toml
import openai
import streamlit as st

# Streamlit secretsから環境変数を読み込む
try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()

# grade_requirementsをStreamlit secretsから読み込む
try:
    grade_requirements_raw = st.secrets["grade_requirements"]
    grade_requirements = {}
    for grade, requirements in grade_requirements_raw.items():
        grade_requirements[grade] = {
            f'requirement{i}': req for i, req in enumerate(requirements.values(), 1)
        }
except KeyError:
    st.error("grade_requirementsが設定されていません。")
    st.stop()

# Streamlitアプリのレイアウト設定
st.set_page_config(page_title="自己評価作成アシスタントツール")
st.title("自己評価作成アシスタントツール")

# 目標等級を選択する
selected_grade = st.selectbox("目指したい等級を選択してください", list(grade_requirements.keys()))

# 選択された等級の要件を表示する
requirements = grade_requirements.get(selected_grade)
if not requirements:
    st.error(f"{selected_grade}に対する要件が見つかりませんでした。")
    st.stop()

st.subheader(f"{selected_grade} の等級要件")
for key, value in requirements.items():
    st.markdown(f'<div class="Requirement-block"><h5>{key}</h5><p class="Requirement-text">{value}</p></div>', unsafe_allow_html=True)

# 各要件に対する実績を入力する
st.subheader(f"{selected_grade} の実績入力")
user_achievements = {}
for key in requirements.keys():
    user_input = st.text_area(f"{key} の実績を入力してください", "")
    if not user_input:
        st.error(f"{key} の実績が入力されていません。")
        st.stop()
    user_achievements[key] = user_input

# 各要件が実績を満たしているか判定する
requirements_met = {}
for key, value in requirements.items():
    if value in user_achievements[key]:
        requirements_met[key] = True
    else:
        requirements_met[key] = False

# 各要件の判定結果を表示する
st.subheader(f"{selected_grade} の判定結果")
for key, value in requirements_met.items():
    if value:
        st.markdown(f"{key}: **要件を満たしています**")
    else:
        st.markdown(f"{key}: **要件を満たしていません**")



