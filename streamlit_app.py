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
if "questions" not in st.session_state:
    st.session_state.questions = questions
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "answered_flags" not in st.session_state:
    st.session_state.answered_flags = [False] * len(st.session_state.questions)
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "mode" not in st.session_state:
    st.session_state.mode = "normal"  # normal, summary

current_questions = st.session_state.questions

# =========================
# ページタイトル
# =========================
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🧠 Python 文法クイズ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px;'>穴埋め形式でPython文法を学習しよう！</p>", unsafe_allow_html=True)
st.divider()

# =========================
# まとめページ
# =========================
if st.session_state.mode == "summary":
    total = len(current_questions)
    correct = st.session_state.correct_count
    rate = round(correct / total * 100, 1)
    
    st.markdown("<h2 style='text-align:center; color:#FF5733;'>📊 結果発表</h2>", unsafe_allow_html=True)
    st.markdown(f"**正解数:** {correct} / {total}")
    st.markdown(f"**正解率:** {rate}%")
    st.progress(rate / 100)
    
    if st.button("🏁 終了"):
        # 状態リセットしてトップページに戻る
        st.session_state.current_index = 0
        st.session_state.answered_flags = [False] * len(current_questions)
        st.session_state.correct_count = 0
        st.session_state.mode = "normal"

# =========================
# 通常問題ページ
# =========================
else:
    idx = st.session_state.current_index
    q = current_questions[idx]
    
    # 進捗バー
    progress = (idx + 1) / len(current_questions)
    st.progress(progress)
    st.markdown(f"**問題 {idx + 1} / {len(current_questions)}**")
    
    # 問題表示
    st.markdown(f"### {q['question']}")
    st.code(q["code"], language="python")
    
    # text_input はユニーク key を使用
    user_answer = st.text_input("空欄を埋めてください", key=f"answer_{idx}")
    
    # ヒント
    with st.expander("💡 ヒントを見る"):
        for i, hint in enumerate(q["hints"], start=1):
            st.info(f"ヒント {i}: {hint}")
    
    # 回答ボタン
    if st.button("✅ 回答する") and not st.session_state.answered_flags[idx]:
        st.session_state.answered_flags[idx] = True
        is_correct = user_answer.strip().lower() == q["answer"].strip().lower()
        
        # Supabaseにログ保存
        supabase.table("quiz_logs").insert({
            "question_id": q["id"],
            "is_correct": is_correct,
            "answered_at": datetime.utcnow().isoformat()
        }).execute()
        
        if is_correct:
            st.session_state.correct_count += 1
            st.success("🎉 正解！")
        else:
            st.error(f"❌ 不正解。正解は: {q['answer']}")
    
    # 解説
    with st.expander("📖 解説を見る"):
        st.write(q["explanation"])
    
    # =========================
    # 次の問題
    # =========================
    if st.button("次の問題 ➡"):
        if st.session_state.current_index < len(current_questions) - 1:
            st.session_state.current_index += 1
        else:
            st.session_state.mode = "summary"
