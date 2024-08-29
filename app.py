import streamlit as st 
from streamlit import _bottom
from utils import casual_responses


st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered", initial_sidebar_state="auto")

# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)

# design elements layouts
st.markdown('<style>div.block-container{padding-top:0.4rem;}</style>', unsafe_allow_html=True)

st.header("*:violet[Chat] Next* ! 💬 ")

with st.expander(label="📋 Tips & Guidance"):
    st.markdown("""
        **Chat to your mind limits without any hesitation, at the same time beware of bot response, they might not be 100 accuract!**
        
        **:green[Enjoy exploring!]**""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: right;">
        <span style="display: inline-block;">Made by- <strong>Yash Keshari,</strong></span>
        <span style="display: inline-block; margin-left: 5px;">
            <a href="https://www.linkedin.com/in/yash907/" target="_blank" style="text-decoration: none; color: blue;">LinkedIn,</a>
            <a href="https://github.com/yash1314" target="_blank" style="text-decoration: none; color: blue; margin-left: 5px;">GitHub</a>
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown(" ")

# initializing chat history 
if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# chat elements 
if prompt := st.chat_input("Chat with your bot",):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(" "):

            res = casual_responses(prompt)
            response = st.write_stream(res)

    st.session_state.messages.append({"role": "assistant", "content": response})
_bottom.button(label='Upload', help='Button to upload file.', use_container_width=False,)
