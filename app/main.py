import os
import toml
import openai
import streamlit as st

# Streamlit secretsから環境変数を読み込む
openai_api_key = st.secrets["openai_api_key"]

# grade_requirementsをStreamlit secretsから読み込む
grade_requirements = st.secrets["grade_requirements"]

# Streamlitアプリのレイアウト設定
st.title("自己評価作成アシスタントツール")

# 目標等級を選択する
selected_grade = st.selectbox("目指したい等級を選択してください", list(grade_requirements.keys()))

# 選択された等級の要件を表示する
st.subheader(f"{selected_grade} の等級要件")
requirements = grade_requirements[selected_grade]
for key, value in requirements.items():
    st.write(f"{key}: {value}")

# 各要件に対する実績を入力する
st.subheader(f"{selected_grade} の実績入力")
user_achievements = {}
for key in requirements.keys():
    user_achievements[key] = st.text_area(f"{key} の実績を入力してください", "")

# 実績の要点を入力
user_input = st.text_area("実績の要点を入力してください:")

if st.button("自己評価文章を生成"):
    # OpenAI APIを使って自己評価文章を生成
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"以下の実績を元に、自己評価を証明する文章を生成してください。\n\n実績:\n{user_input}\n\n自己評価文章:",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    generated_text = response.choices[0].text.strip()
    st.write(generated_text)

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
