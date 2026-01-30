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
    st.session_state.answered = False
    st.session_state.mode = "normal"  # normal, review, summary
    st.session_state.review_questions = []
    st.session_state.total_questions = questions
    st.session_state.correct_count = 0
    st.session_state.logs_buffer = []

# =========================
# 現在の問題セット
# =========================
if st.session_state.mode == "normal":
    current_questions = st.session_state.total_questions
elif st.session_state.mode == "review":
    current_questions = st.session_state.review_questions
else:
    current_questions = []

# =========================
# タイトル
# =========================
st.title("🧠 Python 文法 穴埋めクイズ（軽量ヒント版）")
st.divider()

# =========================
# 通常・復習モードの問題表示
# =========================
if st.session_state.mode in ["normal", "review"] and current_questions:
    # 進捗バー
    progress = (st.session_state.current_index + 1) / len(current_questions)
    st.progress(progress)
    st.markdown(f"**問題 {st.session_state.current_index + 1} / {len(current_questions)}**")

    q = current_questions[st.session_state.current_index]

    st.write(q["question"])
    st.code(q["code"], language="python")

    user_answer = st.text_input("空欄を埋めてください", key=st.session_state.current_index)

    # ヒント（1個だけ）
    if st.button("💡 ヒントを見る") and not st.session_state.answered:
        if q["hints"]:
            st.info(f"ヒント: {q['hints'][0]}")

    # 回答処理
    if st.button("✅ 回答する") and not st.session_state.answered:
        st.session_state.answered = True
        is_correct = user_answer.strip() == q["answer"]

        # 正解カウント
        if is_correct:
            st.success("🎉 正解！")
            st.session_state.correct_count += 1
        else:
            st.error(f"❌ 不正解。正解は: {q['answer']}")
            # 復習対象として追加
            if q not in st.session_state.review_questions:
                st.session_state.review_questions.append(q)

        # ログをバッファに追加
        st.session_state.logs_buffer.append({
            "question_id": q["id"],
            "is_correct": is_correct,
            "answered_at": datetime.utcnow().isoformat()
        })

    # ナビゲーション
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ 前の問題") and st.session_state.current_index > 0:
            st.session_state.current_index -= 1
            st.session_state.answered = False
    with col2:
        if st.button("次の問題 ➡"):
            if st.session_state.current_index < len(current_questions) - 1:
                st.session_state.current_index += 1
                st.session_state.answered = False
            else:
                # 最後の問題を解いたらまとめページへ
                st.session_state.mode = "summary"

# =========================
# まとめページ
# =========================
elif st.session_state.mode == "summary":
    # まとめページでSupabaseにまとめて書き込み
    if st.session_state.logs_buffer:
        for log in st.session_state.logs_buffer:
            supabase.table("quiz_logs").insert(log).execute()
        st.session_state.logs_buffer = []

    total = len(st.session_state.total_questions)
    correct = st.session_state.correct_count
    rate = round(correct / total * 100, 1)

    st.markdown("## 📊 結果発表")
    st.markdown(f"**正解数:** {correct} / {total}")
    st.markdown(f"**正解率:** {rate}%")
    st.progress(rate / 100)

    if st.session_state.review_questions:
        st.markdown("間違えた問題があります。復習モードで再挑戦できます。")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 復習モード"):
                st.session_state.current_index = 0
                st.session_state.mode = "review"
                st.session_state.answered = False
        with col2:
            if st.button("🏁 終了"):
                # ページ状態リセット
                st.session_state.mode = "normal"
                st.session_state.current_index = 0
                st.session_state.answered = False
                st.session_state.review_questions = []
                st.session_state.correct_count = 0
                st.success("トップページに戻りました")
    else:
        st.info("全問正解です！お疲れさまでした 🎉")
        if st.button("🏁 終了"):
            st.session_state.mode = "normal"
            st.session_state.current_index = 0
            st.session_state.answered = False
            st.session_state.review_questions = []
            st.session_state.correct_count = 0
            st.success("トップページに戻りました")

# =========================
# 復習モード終了（復習対象なし）
# =========================
elif st.session_state.mode == "review" and not current_questions:
    st.info("復習モードの問題はありません 🎉")
    if st.button("🏁 終了"):
        st.session_state.mode = "normal"
        st.session_state.current_index = 0
        st.session_state.answered = False
        st.session_state.review_questions = []
        st.session_state.correct_count = 0
        st.success("トップページに戻りました")
