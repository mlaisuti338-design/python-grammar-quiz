import streamlit as st
from datetime import datetime
from supabase import create_client
from question import questions
import openai
import json
import time

# =========================
# RateLimitError 対応
# =========================
try:
    from openai.error import RateLimitError
except ImportError:
    RateLimitError = Exception

# =========================
# OpenAI 設定
# =========================
openai.api_key = st.secrets["OPENAI_API_KEY"]

# =========================
# Supabase 接続
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# プロンプト
# =========================
QUIZ_PROMPT_TEMPLATE = """
あなたはPython初学者向けの教材作成AIです。
以下の条件で「Python文法の穴埋めクイズ」を1問作成してください。

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
# AIクイズ生成（1問ずつ）
# =========================
def generate_one_question():
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": QUIZ_PROMPT_TEMPLATE}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        question = json.loads(content)[0]
        return question
    except RateLimitError:
        st.error("APIの呼び出し制限に達しました。少し時間を置いて再度お試しください。")
        return None
    except Exception as e:
        st.error(f"AI生成中にエラーが発生しました: {e}")
        return None

# =========================
# AI問題をSupabaseに保存
# =========================
def save_ai_quizzes_to_supabase(quizzes):
    for q in quizzes:
        supabase.table("quiz_questions").insert({
            "question": q["question"],
            "code": q["code"],
            "answer": q["answer"],
            "hints": q["hints"],
            "explanation": q["explanation"]
        }).execute()

# =========================
# Supabaseから問題を取得
# =========================
def load_questions_from_supabase():
    try:
        res = supabase.table("quiz_questions").select("*").order("id").execute()
        data = res.data or []
        questions_list = []
        for q in data:
            hints = q.get("hints", [])
            if isinstance(hints, str):
                try:
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
        return questions_list
    except Exception as e:
        st.error(f"Supabase から問題を取得できませんでした: {e}")
        return []

# =========================
# session_state 初期化
# =========================
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.hint_index = 0
    st.session_state.answered = False
    st.session_state.mode = "normal"

if "questions_supabase" not in st.session_state:
    st.session_state.questions_supabase = load_questions_from_supabase()

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "last_ai_generation" not in st.session_state:
    st.session_state.last_ai_generation = 0

if "ai_quizzes_cache" not in st.session_state:
    st.session_state.ai_quizzes_cache = []

# =========================
# タイトル
# =========================
st.title("🧠 Python 文法 穴埋めクイズ（履歴保存・戻れる版）")

# =========================
# 管理者認証
# =========================
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "secret")
password_input = st.text_input("管理者パスワードを入力", type="password")
if password_input:
    if password_input == ADMIN_PASSWORD:
        st.session_state.admin_authenticated = True
        st.success("管理者認証に成功しました")
    else:
        st.session_state.admin_authenticated = False
        st.warning("パスワードが間違っています")

# =========================
# 出題ソース切替
# =========================
source = st.radio("出題する問題セットを選択", ["固定問題", "AI生成問題（Supabase）"])
if source == "固定問題":
    current_questions = questions
else:
    current_questions = st.session_state.questions_supabase
st.session_state.current_questions = current_questions

# =========================
# AI生成ボタン（1問ずつ・管理者のみ・連打防止）
# =========================
if st.session_state.admin_authenticated:
    if time.time() - st.session_state.last_ai_generation < 60:
        st.warning("AI生成は1分に1回までです。少し待ってください。")
    else:
        if st.button("🤖 AIで1問生成して保存"):
            st.session_state.last_ai_generation = time.time()
            with st.spinner("AIが問題を生成しています..."):
                question = generate_one_question()
                if question:
                    st.session_state.ai_quizzes_cache.append(question)
                    save_ai_quizzes_to_supabase([question])
                    st.session_state.questions_supabase = load_questions_from_supabase()
                    st.success("1問生成してSupabaseに保存しました！")

else:
    st.info("AI生成ボタンは管理者のみ使用可能です")

# =========================
# 問題取得
# =========================
if not st.session_state.current_questions:
    st.warning("現在、出題可能な問題がありません。まずAIで問題を生成してください。")
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
        if st.session_state.current_index < len(st.session_state.current_questions) - 1:
            st.session_state.current_index += 1
            st.session_state.hint_index = 0
            st.session_state.answered = False
            st.rerun()

# =========================
# 復習モード
# =========================
st.divider()
if st.button("復習モード"):
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
