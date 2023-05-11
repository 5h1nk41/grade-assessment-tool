import os
import toml
from openai import OpenAI
import openai
import streamlit as st

# TOMLファイルから環境変数を読み込む
config = toml.load("config.toml")
grade_requirements = config["grade_requirements"]
openai_api_key = config["openai_api_key"]

# OpenAI APIの設定
openai.api_key = openai_api_key

# Streamlitアプリのレイアウト設定
st.title("自己評価ツール")
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
