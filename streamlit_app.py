import streamlit as st
import openai

st.set_page_config(page_title="My ChatBot", page_icon="🤖")

# 초기 상태
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "key_submitted" not in st.session_state:
    st.session_state.key_submitted = False

# --- STEP 1: API Key 입력 화면 ---
if not st.session_state.key_submitted:
    st.title("🔑 Enter your OpenAI API Key")
    api_key_input = st.text_input("API Key", type="password")

    if st.button("제출"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.key_submitted = True
            st.success("API Key submitted! Go ahead and chat 👇")
            st.experimental_rerun()
        else:
            st.warning("API Key를 입력해주세요.")

# --- STEP 2: 챗봇 대화 화면 ---
else:
    st.title("💬 My ChatBot")

    # Clear 버튼
    if st.button("Clear"):
        st.session_state.chat_history = []

    # 기존 대화 출력
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    user_input = st.chat_input("Say something...")

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
