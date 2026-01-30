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
st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>🧠 Python 文法クイズ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>穴埋め形式で文法を学習しよう！</p>", unsafe_allow_html=True)
st.divider()

# =========================
# まとめページ
# =========================
if st.session_state.mode == "summary":
    total = len(st.session_state.current_questions)
    correct = st.session_state.correct_count
    rate = round(correct / total * 100, 1)
    
    st.markdown("<h2 style='text-align:center; color:#FF5733;'>📊 結果発表</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>正解数: {correct} / {total} ({rate}%)</p>", unsafe_allow_html=True)
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
    
    # 問題文
    st.write(q["question"])
    st.code(q["code"], language="python")
    
    # 回答入力
    user_answer = st.text_input("空欄を埋めてください", key=idx)
    
    # =========================
    # ヒント（最大2個まで）
    # =========================
    with st.expander("💡 ヒントを見る"):
        # 初回展開時に一つ目のヒントを表示
        if st.session_state.hint_index == 0 and len(q["hints"]) > 0:
            st.session_state.hint_index = 1

        # 現在のヒントを表示（最大2個）
        for i in range(min(st.session_state.hint_index, 2)):
            st.info(f"ヒント {i+1}: {q['hints'][i]}")

        # まだ2個目のヒントが出ていなければボタンを表示
        if st.session_state.hint_index < 2 and len(q["hints"]) > 1:
            if st.button("次のヒント", key=f"hint_btn_{idx}"):
                st.session_state.hint_index = 2
    
    # 回答処理
    if st.button("✅ 回答する", key=f"answer_btn_{idx}") and not st.session_state.answered:
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
            st.session_state.correct_count += 1
            st.success("🎉 正解！")
        else:
            st.error("不正解 😢")
            st.write("正解:", q["answer"])
        with st.expander("📖 解説を見る"):
            st.write(q["explanation"])
    
    # ナビゲーションボタン
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
                st.session_state.mode = "summary"
                st.rerun()
