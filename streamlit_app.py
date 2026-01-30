import streamlit as st
from datetime import datetime
from supabase import create_client
from question import questions  # 固定問題リスト

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
    st.session_state.hint_index = 0
    st.session_state.answered = False
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "mode" not in st.session_state:
    st.session_state.mode = "normal"  # normal or summary

st.session_state.current_questions = questions  # 固定問題のみ使用

# =========================
# タイトル
# =========================
st.title("🧠 Python 文法 穴埋めクイズ（固定問題＋Supabaseログ版）")

# =========================
# まとめページ
# =========================
if st.session_state.mode == "summary":
    total = len(st.session_state.current_questions)
    correct = st.session_state.correct_count
    rate = round(correct / total * 100, 1)
    
    st.markdown("<h2 style='text-align:center; color:#FF5733;'>📊 結果発表</h2>", unsafe_allow_html=True)
    st.markdown(f"**正解数:** {correct} / {total}")
    st.markdown(f"**正解率:** {rate}%")
    st.progress(rate / 100)
    
    if st.button("🏁 トップに戻る"):
        # 状態リセット
        st.session_state.current_index = 0
        st.session_state.hint_index = 0
        st.session_state.answered = False
        st.session_state.correct_count = 0
        st.session_state.mode = "normal"

# =========================
# 通常問題ページ
# =========================
else:
    idx = st.session_state.current_index
    q = st.session_state.current_questions[idx]
    
    # 進捗バー
    total_questions = len(st.session_state.current_questions)
    progress_value = (idx + 1) / total_questions
    st.progress(progress_value)
    st.markdown(f"**問題 {idx + 1} / {total_questions}**")
    
    # 問題表示
    st.write(q["question"])
    st.code(q["code"], language="python")
    user_answer = st.text_input("空欄を埋めてください", key=idx)
    
    # ヒント
    if st.button("ヒントを見る"):
        if st.session_state.hint_index < len(q["hints"]):
            st.session_state.hint_index += 1

    for i in range(st.session_state.hint_index):
        st.info(f"ヒント {i+1}: {q['hints'][i]}")
    
    # 回答処理
    if st.button("回答する") and not st.session_state.answered:
        st.session_state.answered = True
        is_correct = user_answer.strip() == q["answer"]

        # Supabase にログを保存
        try:
            supabase.table("quiz_logs").insert({
                "question_id": q["id"],
                "is_correct": is_correct,
                "answered_at": datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            st.error(f"ログ保存でエラー: {e}")

        if is_correct:
            st.success("正解！🎉")
            st.session_state.correct_count += 1
        else:
            st.error("不正解 😢")
            st.write("正解:", q["answer"])
        st.info(q["explanation"])
    
    # 問題移動ボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 前の問題"):
            if idx > 0:
                st.session_state.current_index -= 1
                st.session_state.hint_index = 0
                st.session_state.answered = False
                st.rerun()
    with col2:
        if st.button("次の問題 →"):
            if idx < total_questions - 1:
                st.session_state.current_index += 1
                st.session_state.hint_index = 0
                st.session_state.answered = False
                st.rerun()
            else:
                # 最後の問題ならまとめページに切り替え
                st.session_state.mode = "summary"
                st.rerun()
