import os
import toml
import openai
import streamlit as st

def generate_self_evaluation(performance, grade_requirements):
    prompt = f"実績: {performance}\n要件: {grade_requirements}\n自己評価の証明をするような納得感のある文章を生成し、等級要件を満たしているか判定してください。判定結果のロジックを説明し、満たしていない場合は、どのような実績を積み上げれば達成できるのかアドバイスを提供してください。"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def assess_performance(performance, requirement):
    prompt = f"実績: {performance}\n要件: {requirement}\nこの実績は要件を満たしているか多角的な視点で厳しく判定してください。判定結果の根拠を論理的に説明してください。"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.1,
    )
    return response.choices[0].text.strip()

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
            key: value for key, value in requirements.items()
        }
except KeyError:
    st.error("grade_requirementsが設定されていません。")
    st.stop()

# Streamlitアプリのレイアウト設定
st.set_page_config(page_title="自己評価作成アシスタントツール")
st.title("自己評価作成アシスタントツール")

# ドロップダウンメニューで評価対象の等級を選択
selected_grade = st.selectbox("評価対象の等級を選択してください", list(grade_requirements.keys()))

# 選択された等級の要件を表示
st.header(f"{selected_grade}の要件")
selected_requirement = st.selectbox("選択したい要件を選んでください", list(grade_requirements[selected_grade].keys()))

# 実績入力
st.header("実績入力")
performance = {}
for requirement in grade_requirements[selected_grade]:
    performance[requirement] = st.text_area(f"{requirement} の実績を入力してください。", height=100)

# 要件判定ボタン
if st.button("自己評価を生成して判定を実行"):

    missing_inputs = [req for req, value in performance.items() if not value]
    if missing_inputs:
        st.error(f"{', '.join(missing_inputs)} の実績が入力されていません。")
    else:
        with st.spinner("判定中..."):
            # ここで実績をまとめ、自己評価の証明をするような文章を生成し、等級要件を満たしているか判定する
            result = generate_self_evaluation(performance, grade_requirements[selected_grade])
            st.write(result)
