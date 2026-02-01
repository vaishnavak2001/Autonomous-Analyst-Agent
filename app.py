import streamlit as st
import os
from agent_backend import get_agent_response

# page config
st.set_page_config(
    page_title="Pandas Data Analysis with LLM",
    page_icon="📊")
st.title("the Analyst Agent")
st.caption("I can analyze data (Titanic) and search the web (DuckDuckGo). ")
if "messages" not in st.session_state:
    st.session_state.messages = []
#sidebar
with st.sidebar:
    st.header("Tools Available")
    st.write("1 pandas data analysis on Titanic dataset.")
    st.write("2 Web search using DuckDuckGo.")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
#Display chat messages from history 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"])
if prompt := st.chat_input("Ask me anything about Titanic data or general knowledge!"):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking...(Routing and executing)"):
            try:
                response_text, image_path, source = get_agent_response(prompt)
                st.markdown(response_text)
                if image_path:
                    st.image(image_path)
                    st.success("Chart generated!")
                st.caption(f"Response source: {source}")
                # save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "image": image_path
                })
            except Exception as e:
                st.error(f"Error: {e}")

