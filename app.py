import random, time, sys
import streamlit as st 
from streamlit import _bottom
from better_profanity import profanity
from src.logging import logging
from src.exception import CustomException

from utils import message_prompt, stream_output
from src.model_components.model import Model

# page setup
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)

# design elements layouts
st.markdown('<style>div.block-container{padding-top:0.4rem;}</style>', unsafe_allow_html=True)

st.header(f"*:orange[Chat] Next*! 💬",divider='orange')
st.markdown(" ")
st.markdown("""**Feel free to chat openly and ask anything you like. Just keep in mind that bot responses might not always be factual and 100% accurate, so use carefully.
    <span style="color: green;">Enjoy exploring!</span>**""", unsafe_allow_html=True)

# details about creator profile
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
st.markdown(" ")


# initializing message history 
if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# chat elements 
if prompt := st.chat_input("Chat with bot",):
    try: 
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    except Exception as e:
        logging.info("Error in user message input")
        CustomException(e, sys)
    
    with st.chat_message("assistant"):
        try:
            # filtering out explicit user prompts
            if profanity.contains_profanity(prompt):  
                res = random.choice(["Sorry, I cannot assist with that!",
                                    "I cannot help with that. Please, Let me know how I can assist further."])
                st.write_stream(stream_output(res)) 
                    
            else:
                with st.spinner("Thinking..."):
                    start_time = time.monotonic()

                    res = Model.model_generate(message=prompt)
                    st.write_stream(stream_output(res)) 
                    
                    processed_time = round(time.monotonic() - start_time, ndigits=2)
                    st.markdown(f'<div style="text-align: right;">Processed time: {processed_time} seconds</div>',
                                unsafe_allow_html=True)
        except Exception as e:
            logging.info('Error generated in model output generation')
            CustomException(e, sys)

    st.session_state.messages.append({"role": "assistant", "content": res})