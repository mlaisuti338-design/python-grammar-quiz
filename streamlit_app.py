import streamlit as st
import random
from datetime import datetime
from supabase import create_client
from question import questions

# =========================
# Supabase 接続
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("🧠 Python 文法 穴埋めクイズ（履歴保存版）")

# =========================
# 初期化
# =========================
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(questions)
    st.session_state.hint_index = 0
    st.session_state.answered = False

q = st.session_state.current_q

# =========================
# 問題表示
# =========================
st.write(q["question"])
st.code(q["code"], language="python")

user_answer = st.text_input("空欄を埋めてください")

# =========================
# ヒント
# =========================
if st.button("ヒントを見る"):
    if st.session_state.hint_index < len(q["hints"]):
        st.session_state.hint_index += 1

for i in range(st.session_state.hint_index):
    st.info(f"ヒント {i+1}: {q['hints'][i]}")

# =========================
# 回答処理（Supabase保存）
# =========================
if st.button("回答する") and not st.session_state.answered:
    st.session_state.answered = True

    is_correct = user_answer.strip() == q["answer"]

    # Supabase に保存
    supabase.table("quiz_logs").insert({
        "question_id": q["id"],
        "is_correct": is_correct,
        "answered_at": datetime.utcnow().isoformat()
    }).execute()

    if is_correct:
        st.success("正解！🎉")
    else:
        st.error("不正解 😢")
        st.write("正解:", q["answer"])

    st.info(q["explanation"])

# =========================
# 次の問題
# =========================
if st.button("次の問題"):
    st.session_state.current_q = random.choice(questions)
    st.session_state.hint_index = 0
    st.session_state.answered = False
    st.rerun()

# =========================
# 復習モード（不正解履歴）
# =========================
st.divider()
if st.button("復習モード"):
    res = supabase.table("quiz_logs") \
        .select("question_id") \
        .eq("is_correct", False) \
        .execute()

    wrong_ids = {row["question_id"] for row in res.data}

    wrongs = [qq for qq in questions if qq["id"] in wrong_ids]

    if wrongs:
        st.session_state.current_q = random.choice(wrongs)
        st.session_state.hint_index = 0
        st.session_state.answered = False
        st.rerun()
    else:
        st.info("復習する問題はありません 🎉")
