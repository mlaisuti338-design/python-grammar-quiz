import streamlit as st
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

# =========================
# session_state 初期化
# =========================
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.answered = False
    st.session_state.mode = "normal"

if "questions_supabase" not in st.session_state:
    st.session_state.questions_supabase = questions

current_questions = st.session_state.questions_supabase

# =========================
# ページタイトル & 説明
# =========================
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🧠 Python 文法クイズ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px;'>穴埋め形式でPython文法を学習しよう！</p>", unsafe_allow_html=True)
st.divider()

# =========================
# 進捗バー
# =========================
progress = (st.session_state.current_index + 1) / len(current_questions)
st.progress(progress)
st.markdown(f"**問題 {st.session_state.current_index + 1} / {len(current_questions)}**")

# =========================
# 現在の問題表示
# =========================
q = current_questions[st.session_state.current_index]

st.markdown(f"### {q['question']}")
st.code(q["code"], language="python")

user_answer = st.text_input("空欄を埋めてください", key=st.session_state.current_index)

# =========================
# ヒントを折りたたみ表示
# =========================
with st.expander("💡 ヒントを見る"):
    for i, hint in enumerate(q["hints"], start=1):
        st.info(f"ヒント {i}: {hint}")

# =========================
# 回答処理
# =========================
if st.button("✅ 回答する") and not st.session_state.answered:
    st.session_state.answered = True
    is_correct = user_answer.strip() == q["answer"]
    supabase.table("quiz_logs").insert({
        "question_id": q["id"],
        "is_correct": is_correct,
        "answered_at": datetime.utcnow().isoformat()
    }).execute()
    if is_correct:
        st.success("🎉 正解！")
    else:
        st.error(f"❌ 不正解。正解は: {q['answer']}")

# =========================
# 解説を折りたたみ
# =========================
with st.expander("📖 解説を見る"):
    st.write(q["explanation"])

# =========================
# ナビゲーションボタン（横並び・カラー）
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("⬅ 前の問題"):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
            st.session_state.answered = False
            st.rerun()
with col2:
    if st.button("次の問題 ➡"):
        if st.session_state.current_index < len(current_questions) - 1:
            st.session_state.current_index += 1
            st.session_state.answered = False
            st.rerun()
with col3:
    if st.button("🔄 復習モード"):
        res = supabase.table("quiz_logs").select("question_id").eq("is_correct", False).execute()
        wrong_ids = {row["question_id"] for row in res.data}
        wrongs = [i for i, qq in enumerate(current_questions) if qq["id"] in wrong_ids]
        if wrongs:
            st.session_state.current_index = wrongs[0]
            st.session_state.answered = False
            st.session_state.mode = "review"
            st.rerun()
        else:
            st.info("復習する問題はありません 🎉")
