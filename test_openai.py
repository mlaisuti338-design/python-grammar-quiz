import streamlit as st
import openai

# OpenAI APIキーをセット
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("OpenAI API テスト")

st.write("テスト用のボタンを押すと、AIがHello表示コードを返します")

if st.button("AIに問い合わせ"):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "PythonでHelloと表示するコードを1行だけ教えて"}],
            temperature=0
        )
        st.write("AIの返答:")
        st.code(response.choices[0].message.content, language="python")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

