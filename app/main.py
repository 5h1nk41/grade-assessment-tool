import os
import toml
import openai
import streamlit as st

def generate_self_evaluation(performance, requirement):
    performance_list = "\n".join([f"- {key}: {value}" for key, value in performance.items()])
    requirement_list = "\n".join([f"- {key}: {value}" for key, value in requirement.items()])

    prompt = f"実績: {performance_list}\n要件: {requirement_list}\nこの実績に基づいて、納得感のある自己評価を生成し、等級要件を満たしているか判定してください。判定結果の根拠を論理的に説明し、満たしていない場合は達成のためのアドバイスを提供してください。"

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
selected_requirement = st.selectbox("選択したい要件を選んでください", list(grade_requirements[selected_grade].keys()))
st.subheader(selected_requirement)
st.write(grade_requirements[selected_grade][selected_requirement])

# 実績入力
st.header("実績入力")
performance = st.text_area(f"{selected_requirement} の実績を入力してください。", height=100)

# 要件判定ボタン
if st.button("自己評価を生成して判定を実行"):

    if not performance:
        st.error(f"{selected_requirement} の実績が入力されていません。")
    else:
        with st.spinner("判定中..."):
            # ここで実績をまとめ、自己評価の証明をするような文章を生成し、等級要件を満たしているか判定する
            result = generate_self_evaluation({selected_requirement: performance}, {selected_requirement: grade_requirements[selected_grade][selected_requirement]})
            st.write(result)
            st.subheader("生成された自己評価文章")
            st.write(result.split("\n")[0])  # 生成された文章を取り出して表示する
