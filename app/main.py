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
    grade_requirements = st.secrets["grade_requirements"]
except KeyError:
    st.error("grade_requirementsが設定されていません。")
    st.stop()

# Streamlitアプリのレイアウト設定
st.set_page_config(page_title="自己評価作成アシスタントツール")
st.title("自己評価作成アシスタントツール")

# 目標等級を選択する
if "grade_requirements" not in locals():
    st.error("grade_requirementsが設定されていません。")
    st.stop()

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


if st.button("自己評価文章を生成"):
    with st.spinner("自己評価文章を生成中..."):
        # OpenAI APIを使って文章を生成
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"以下の実績を元に、自己評価を証明する文章を生成してください。各実績ごとに等級要件の何をを満たしているか、補足してください。\n\n実績:\n{user_achievements}\n\n自己評価文章:",
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        if not response.choices:
            st.error("自己評価文章を生成できませんでした。")
            st.stop()

        generated_text = response.choices[0].text.strip()

    # 生成された自己評価文章が等級要件を満たすか判断
    grade_met = None
    for grade, requirements in grade_requirements.items():
        met_requirements = all(req in generated_text for req in requirements.values())
        if met_requirements:
            grade_met = grade
            break

    if grade_met:
        st.success(f"生成された自己評価文章は{grade_met}の要件を満たしています。")
    else:
        st.warning("生成された自己評価文章は、対象となる等級の要件を満たしていません。")
