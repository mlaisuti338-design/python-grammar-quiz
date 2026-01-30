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

st.session_state.current_questions = questions

# =========================
# タイトル
# =========================
st.markdown("<h1 style='text-align:center; color:#4B8BBE; font-size:36px;'>🧠 Python 文法クイズ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; color:gray;'>穴埋め形式で文法を学習しよう！</p>", unsafe_allow_html=True)
st.divider()

# =========================
# まとめページ
# =========================
if st.session_state.mode == "summary":
    total = len(st.session_state.current_questions)
    correct = st.session_state.correct_count
    rate = round(correct / total * 100, 1)
    
    st.markdown("<h2 style='text-align:center; color:#FF5733;'>📊 結果発表</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:18px;'>正解数: {correct} / {total} ({rate}%)</p>", unsafe_allow_html=True)
    st.progress(rate / 100)

    if correct == total:
        st.balloons()
        st.success("🎉 全問正解！おめでとう！🎉")
    
    if st.button("🏁 トップに戻る"):
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
    total_questions = len(st.session_state.current_questions)
    
    # 進捗バー
    progress_value = (idx + 1) / total_questions
    st.progress(progress_value)
    st.markdown(f"<p style='text-align:center;'>問題 {idx + 1} / {total_questions} ({int(progress_value*100)}%)</p>", unsafe_allow_html=True)
    
    # 問題表示
    with st.container():
        st.markdown(f"<h3 style='color:#FF6F61;'>{q['question']}</h3>", unsafe_allow_html=True)
        st.code(q["code"], language="python")
    
    # 回答入力
    user_answer = st.text_input("空欄を埋めてください", key=idx)
    
    # ヒント
    if st.button("💡 ヒントを見る"):
        if st.session_state.hint_index < len(q["hints"]):
            st.session_state.hint_index += 1
    for i in range(st.session_state.hint_index):
        st.info(f"ヒント {i+1}: {q['hints'][i]}")
    
    # 回答処理
    if st.button("✅ 回答する") and not st.session_state.answered:
        st.session_state.answered = True
        is_correct = user_answer.strip() == q["answer"]

        # Supabaseログ保存
        try:
            supabase.table("quiz_logs").insert({
                "question_id": q["id"],
                "is_correct": is_correct,
                "answered_at": datetime.utcnow().isoformat()
            }).execute()
        except Exception as e:
            st.error(f"ログ保存でエラー: {e}")

        if is_correct:
            st.session_state.correct_count += 1
            st.success("🎉 正解！")
        else:
            st.error("不正解 😢")
            st.write("正解:", q["answer"])
        st.info(q["explanation"])
    
    # ナビゲーション
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ 前の問題"):
            if idx > 0:
                st.session_state.current_index -= 1
                st.session_state.hint_index = 0
                st.session_state.answered = False
                st.rerun()
    with col2:
        if st.button("次の問題 ➡"):
            if idx < total_questions - 1:
                st.session_state.current_index += 1
                st.session_state.hint_index = 0
                st.session_state.answered = False
                st.rerun()
            else:
                # 最後の問題ならまとめページへ
                st.session_state.mode = "summary"
                st.rerun()
