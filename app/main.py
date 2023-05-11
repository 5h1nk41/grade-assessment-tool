import os
import toml
import openai
import streamlit as st

def assess_performance(performance, requirement):
    prompt = '''
    f"実績: {performance}\n要件: {requirement}\nこの実績は要件を満たしているか多角的な視点で厳しく判定してください。
    判定結果の根拠を説明してください。実績のサマリを説明してください。"
    '''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
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
for requirement, content in grade_requirements[selected_grade].items():
    st.subheader(requirement)
    st.write(content)

# 実績入力
st.header("実績入力")
performance = {}
for requirement in grade_requirements[selected_grade]:
    performance[requirement] = st.text_area(f"{requirement} の実績を入力してください。", height=100)

# 要件判定ボタン
assessment_results = {}
for requirement in grade_requirements[selected_grade]:
    if st.button(f"{requirement} の判定を実行", key=f"assessment_{requirement}"):

        if not performance[requirement]:
            st.error(f"{requirement} の実績が入力されていません。")
        else:
            with st.spinner("判定中..."):
                # ここで実績と要件を比較して判定を行う
                result = assess_performance(performance[requirement], grade_requirements[selected_grade][requirement])
                st.write(result)
