import streamlit as st
import openai

st.set_page_config(page_title="My ChatBot", page_icon="🤖")

# --- API Key 저장 ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- Chat 기록 초기화 ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- API Key 입력창 (입력되면 숨김 처리) ---
if not st.session_state.api_key:
    st.title("🔑 Enter your OpenAI API Key")
    api_key_input = st.text_input("API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.experimental_rerun()
else:
    # --- Chat 화면 ---
    st.title("💬 My ChatBot")
    
    # Clear 버튼
    if st.button("Clear"):
        st.session_state.chat_history = []

    # 채팅 메시지 출력
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # 사용자 입력
    user_input = st.chat_input("What is up?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        try:
            client = openai.OpenAI(api_key=st.session_state.api_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=st.session_state.chat_history,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.experimental_rerun()
