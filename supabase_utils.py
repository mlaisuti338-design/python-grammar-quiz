from supabase import create_client
import streamlit as st

# Supabase クライアント作成
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def fetch_questions(limit=50):
    """
    Supabaseから問題を取得する
    """
    response = (
        supabase
        .table("questions")
        .select("*")
        .limit(limit)
        .execute()
    )
    return response.data


def insert_questions(questions):
    """
    問題リストをSupabaseに保存する
    questions: list[dict]
    """
    if not questions:
        return

    supabase.table("questions").insert(questions).execute()

