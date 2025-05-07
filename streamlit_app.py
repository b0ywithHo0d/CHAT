import streamlit as st
import openai

st.set_page_config(page_title="My ChatBot", page_icon="🤖")

# 초기 상태 설정
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- STEP 1: API Key 입력 페이지 ---
if not st.session_state.api_key:
    st.title("🔑 Enter your OpenAI API Key")
    api_key_input = st.text_input("API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("API Key received! You can now chat 👇")
        st.stop()  # 입력 직후에는 stop으로 종료 → 다음 실행에서 채팅 UI 보임

# --- STEP 2: Chat 화면 ---
st.title("💬 My ChatBot")

# Clear 버튼
if st.button("Clear"):
    st.session_state.chat_history = []

# 기존 대화 출력
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
user_input = st.chat_input("Say something...")

# 입력이 있으면 GPT-4 호출
if user_input:
    # 사용자 메시지 저장
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # OpenAI API 호출
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

    # 응답 저장
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
