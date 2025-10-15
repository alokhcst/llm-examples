from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    except Exception as e:
        # Don't let the whole app crash on network / API errors. Show a helpful message instead.
        st.error("Failed to contact the OpenAI API. Check your network and API key.")
        st.exception(e)
        # Optionally add a diagnostic assistant message so the chat stays consistent.
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Sorry — I couldn't reach the OpenAI API. Please check your internet connection and that your API key is correct."
        })
        st.chat_message("assistant").write(st.session_state.messages[-1]["content"])
    else:
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
