import os
import toml
import openai
import streamlit as st

# 実績から自己評価の文章をAIで生成
def generate_self_evaluation(performance, requirement):
    requirement_list = "\n".join([f"- {key}: {value}" for key, value in requirement.items()])

    # 実績をリストに変換
    performance_lines = performance.split("\n")
    performance_list = "\n".join([f"- {line}" for line in performance_lines])

    prompt = f"以下の実績に基づいて、自己評価の証明をするような納得感のある文章を生成してください。\n\n実績:\n{performance_list}\n\n要件:\n{requirement_list}\n\n自己評価文章:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # ログ出力
    st.write(f"Prompt: {prompt}")
    st.write(f"Response: {response}")
    
    return response.choices[0].text.strip()

# 自己評価の文章と等級要件を照らし合わせ、AIで等級要件を満たしているか判定
def assess_performance(performance, requirement):
    prompt = f"以下の実績と要件を比較し、実績が要件を満たしているかどうか判断してください。\n\n実績:\n- {performance}\n\n要件:\n- {requirement}\n\n判断:"

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

# ドロップダウンメニューで評価対象の要件を選択
selected_requirement = st.selectbox("評価対象の要件を選択してください", list(grade_requirements[selected_grade].keys()))

# 選択された要件の内容を表示
st.header(f"{selected_requirement} の要件")
st.write(grade_requirements[selected_grade][selected_requirement])

# 実績入力
st.header("実績入力")
performance = st.text_area(f"{selected_requirement} の実績を入力してください。", height=100)

generated_evaluation = ""

# 自己評価文章生成
if st.button("自己評価文章を生成"):
    if not performance:
        st.error(f"{selected_requirement} の実績が入力されていません。")
    else:
        with st.spinner("文章生成中..."):
            generated_evaluation = generate_self_evaluation(performance, {selected_requirement: grade_requirements[selected_grade][selected_requirement]})
            if not generated_evaluation:
                st.write("自己評価文章が生成されませんでした。")

# 実績入力
st.header("自己評価文章")
evaluation_input = st.text_area("生成された自己評価文章がここに表示されます。", value=generated_evaluation, height=100)

# 要件判定ボタン
if st.button("要件判定を実行"):
    if not evaluation_input:
        st.error("自己評価文章が入力されていません。")
    else:
        with st.spinner("判定中..."):
            result = assess_performance(evaluation_input, grade_requirements[selected_grade][selected_requirement])
            st.subheader("判定結果")
            st.write(result)

