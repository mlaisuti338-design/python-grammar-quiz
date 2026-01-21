import streamlit as st
import random
from question import questions

st.title("🧠 Python 文法 穴埋めクイズ")

# 初期化
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(questions)
    st.session_state.hint_index = 0
    st.session_state.answered = False
    st.session_state.wrong_ids = set()

q = st.session_state.current_q

st.write(q["question"])
st.code(q["code"], language="python")

user_answer = st.text_input("空欄を埋めてください")

# ヒント
if st.button("ヒントを見る"):
    if st.session_state.hint_index < len(q["hints"]):
        st.session_state.hint_index += 1

for i in range(st.session_state.hint_index):
    st.info(f"ヒント {i+1}: {q['hints'][i]}")

# 回答
if st.button("回答する") and not st.session_state.answered:
    st.session_state.answered = True
    if user_answer.strip() == q["answer"]:
        st.success("正解！")
    else:
        st.error("不正解")
        st.write("正解:", q["answer"])
        st.session_state.wrong_ids.add(q["id"])

    st.info(q["explanation"])

# 次の問題
if st.button("次の問題"):
    st.session_state.current_q = random.choice(questions)
    st.session_state.hint_index = 0
    st.session_state.answered = False

# 復習
st.divider()
if st.button("復習モード"):
    wrongs = [qq for qq in questions if qq["id"] in st.session_state.wrong_ids]
    if wrongs:
        st.session_state.current_q = random.choice(wrongs)
        st.session_state.hint_index = 0
        st.session_state.answered = False
    else:
        st.info("復習する問題はありません 🎉")
