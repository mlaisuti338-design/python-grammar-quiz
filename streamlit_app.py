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
    st.session_state.hint_index = 0
    st.session_state.answered = False
    st.session_state.mode = "normal"

if "questions_supabase" not in st.session_state:
    # Supabaseから問題をロード
    try:
        res = supabase.table("quiz_questions").select("*").order("id").execute()
        data = res.data or []
        questions_list = []
        for q in data:
            hints = q.get("hints", [])
            if isinstance(hints, str):
                try:
                    import json
                    hints = json.loads(hints)
                except:
                    hints = []
            questions_list.append({
                "id": q.get("id", 0),
                "question": q.get("question", ""),
                "code": q.get("code", ""),
                "answer": q.get("answer", ""),
                "hints": hints,
                "explanation": q.get("explanation", "")
            })
        st.session_state.questions_supabase = questions_list
    except Exception as e:
        st.error(f"Supabase から問題を取得できませんでした: {e}")
        st.session_state.questions_supabase = []

# =========================
# タイトル
# =========================
st.title("🧠 Python 文法 穴埋めクイズ（Supabase対応版）")

# =========================
# 出題ソース切替（固定問題 or Supabase）
# =========================
source = st.radio("出題する問題セットを選択", ["固定問題", "Supabase問題"])
if source == "固定問題":
    current_questions = questions
else:
    current_questions = st.session_state.questions_supabase
st.session_state.current_questions = current_questions

# =========================
# 問題取得
# =========================
if not st.session_state.current_questions:
    st.warning("現在、出題可能な問題がありません。")
    st.stop()

q = st.session_state.current_questions[st.session_state.current_index]

# =========================
# 問題表示
# =========================
st.write(q["question"])
st.code(q["code"], language="python")
user_answer = st.text_input("空欄を埋めてください", key=st.session_state.current_index)

# =========================
# ヒント
# =========================
if st.button("ヒントを見る"):
    if st.session_state.hint_index < len(q["hints"]):
        st.session_state.hint_index += 1

for i in range(st.session_state.hint_index):
    st.info(f"ヒント {i+1}: {q['hints'][i]}")

# =========================
# 回答処理
# =========================
if st.button("回答する") and not st.session_state.answered:
    st.session_state.answered = True
    is_correct = user_answer.strip() == q["answer"]
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
    else:
        st.error("不正解 😢")
        st.write("正解:", q["answer"])
    st.info(q["explanation"])

# =========================
# ナビゲーション
# =========================
col1, col2 = st.columns(2)
with col1:
    if st.button("← 前の問題"):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
            st.session_state.hint_index = 0
            st.session_state.answered = False
            st.rerun()
with col2:
    if st.button("次の問題 →"):
        if st.session_state.current_index < len(st.session_state.current_questions) - 1:
            st.session_state.current_index += 1
            st.session_state.hint_index = 0
            st.session_state.answered = False
            st.rerun()

# =========================
# 復習モード（不正解問題のみ）
# =========================
st.divider()
if st.button("復習モード"):
    try:
        res = supabase.table("quiz_logs").select("question_id").eq("is_correct", False).execute()
        wrong_ids = {row["question_id"] for row in res.data}
        wrongs = [i for i, qq in enumerate(st.session_state.current_questions) if qq["id"] in wrong_ids]
        if wrongs:
            st.session_state.current_index = wrongs[0]
            st.session_state.hint_index = 0
            st.session_state.answered = False
            st.session_state.mode = "review"
            st.rerun()
        else:
            st.info("復習する問題はありません 🎉")
    except Exception as e:
        st.error(f"復習モード取得でエラー: {e}")
