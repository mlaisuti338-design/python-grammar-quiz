import streamlit as st
from datetime import datetime
from supabase import create_client
from question import questions
import openai
import json

# =========================
# OpenAI 設定
# =========================
openai.api_key = st.secrets["OPENAI_API_KEY"]

QUIZ_PROMPT = """
あなたはPython初学者向けの教材作成AIです。
以下の条件で「Python文法の穴埋めクイズ」を5問作成してください。

条件:
- 難易度: 初学者
- 各問題は穴埋め形式（_____）
- 日本語で出力
- 出力は必ずJSONのみ（説明文は禁止）

JSON形式:
[
  {
    "id": 1,
    "question": "次のコードの空欄を埋めてください。",
    "code": "print(_____)",
    "answer": "'Hello'",
    "hints": [
      "文字列を表示します",
      "クォーテーションで囲みます"
    ],
    "explanation": "print関数で文字列を表示できます。"
  }
]
"""

# =========================
# AIクイズ生成関数
# =========================
def generate_ai_quiz():
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": QUIZ_PROMPT}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)

# =========================
# AIクイズをSupabaseに保存（③-2 ここ）
# =========================
def save_ai_quiz_to_supabase(quizzes):
    for q in quizzes:
        supabase.table("quiz_questions").insert({
            "question": q["question"],
            "code": q["code"],
            "answer": q["answer"],
            "hints": q["hints"],
            "explanation": q["explanation"]
        }).execute()

# =========================
# Supabase 接続
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# Supabaseから問題を取得
# =========================
def load_questions_from_supabase():
    res = supabase.table("quiz_questions") \
        .select("*") \
        .order("id") \
        .execute()

    # Supabaseの配列型(hints)はそのままPythonのlistとして返る場合と文字列になる場合があるので調整
    questions = []
    for q in res.data:
        hints = q["hints"]
        # 文字列になっていた場合はJSONとしてロード
        if isinstance(hints, str):
            hints = json.loads(hints)
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "code": q["code"],
            "answer": q["answer"],
            "hints": hints,
            "explanation": q["explanation"]
        })
    return questions

st.title("🧠 Python 文法 穴埋めクイズ（履歴保存・戻れる版）")

# =========================
# 出題ソース切替UI
# =========================
source = st.radio("出題する問題セットを選択", ["固定問題", "AI生成問題（Supabase）"])

if source == "固定問題":
    current_questions = questions
else:
    current_questions = st.session_state.questions_supabase

# session_stateのcurrent_questionsにセット
st.session_state.current_questions = current_questions


# =========================
# 🤖 AI生成＆保存ボタン（③-2 本体）
# =========================
if st.button("🤖 AIでクイズを生成して保存"):
    with st.spinner("AIがクイズを生成しています..."):
        quizzes = generate_ai_quiz()
        save_ai_quiz_to_supabase(quizzes)

    st.success("AIクイズをSupabaseに保存しました！")

# =========================
# 初期化
# =========================
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.hint_index = 0
    st.session_state.answered = False
    st.session_state.mode = "normal"

# =========================
# session_state にSupabase問題をロード
# =========================
if "questions_supabase" not in st.session_state:
    st.session_state.questions_supabase = load_questions_from_supabase()

# =========================
# 問題取得（今はまだ question.py）
# =========================
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
# 回答処理（Supabase保存）
# =========================
if st.button("回答する") and not st.session_state.answered:
    st.session_state.answered = True

    is_correct = user_answer.strip() == q["answer"]

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
        if st.session_state.current_index < len(questions) - 1:
            st.session_state.current_index += 1
            st.session_state.hint_index = 0
            st.session_state.answered = False
            st.rerun()

# =========================
# 復習モード
# =========================
st.divider()

if st.button("復習モード"):
    res = supabase.table("quiz_logs") \
        .select("question_id") \
        .eq("is_correct", False) \
        .execute()

    wrong_ids = {row["question_id"] for row in res.data}
    wrongs = [i for i, qq in enumerate(questions) if qq["id"] in wrong_ids]

    if wrongs:
        st.session_state.current_index = wrongs[0]
        st.session_state.hint_index = 0
        st.session_state.answered = False
        st.session_state.mode = "review"
        st.rerun()
    else:
        st.info("復習する問題はありません 🎉")
