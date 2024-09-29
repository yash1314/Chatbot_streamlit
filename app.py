import random, time, sys
import streamlit as st 
from streamlit import _bottom
from better_profanity import profanity
from src.logging import logging

from utils import message_prompt, stream_output, app_info
from src.model_components.model import Model
from PIL import Image
from streamlit_lottie import st_lottie_spinner
from artifact.animations.lottie_animation import animation2
# page setup
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)


# design elements layouts
st.markdown('<style>div.block-container{padding-top:0.4rem;}</style>', unsafe_allow_html=True)

st.header(f"*:orange[Chat]Next*! 💬", divider="gray")

with st.form('App info', border= False):
    app_button = st.form_submit_button(label="Start Here")
    if app_button:
        app_info()

# st.markdown(" ")
# st.markdown("""**Feel free to chat openly and ask anything you like. Just keep in mind that bot responses might not always be factual and 100% accurate, so use carefully.
#     <span style="color: green;">Enjoy exploring!</span>**""", unsafe_allow_html=True)

# # details about creator profile 
# with st.popover(label="Developer Profile"):
#     with st.container(border=True):
#         st.markdown("<h4 style='text-align: center; color:#f08080;'>YASH KESHARI</h4>", unsafe_allow_html=True)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.link_button("**LinkedIn**", "https://www.linkedin.com/in/yash907", use_container_width=True)
#         with col2:
#             st.link_button("**GitHub**", "https://github.com/yash1314", use_container_width=True)


st.markdown(" ")
        
st.markdown(" ")

# images and lottie animations
bot_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/chatbot.png"
user_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/man.png"


# initializing message history 
if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", 
                                        "content": "Hi User! I am a smart AI. How can I help you today?"}]

for message in st.session_state.messages:
    if message['role'] == 'user':
        with st.chat_message(message["role"], avatar=user_img):
            st.markdown(message["content"])
    elif message['role'] == 'assistant':
        with st.chat_message(message["role"], avatar=bot_img):
            st.markdown(message["content"])


# chat elements 
if prompt := st.chat_input("Chat with bot"):
     
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_img):
        st.markdown(prompt)
    
    with st.chat_message("assistant",avatar=bot_img):
        message_placeholder = st.empty()
        try: 
            if profanity.contains_profanity(prompt):  
                res = random.choice(["Sorry, but I cannot assist with that!",
                                    "I cannot help with that. Please, Let me know how I can assist further."])
                res = message_placeholder.write_stream(stream_output(res))
                latency=4
                st.markdown(f'<div style="text-align: right;">Latency: {latency} seconds</div>', unsafe_allow_html=True)

            else:
                # with st.spinner("Thinking..."):
                with st_lottie_spinner(animation2(), height=52, width=55):
                    start_time = time.monotonic()
                    res = Model.model_generate(message=prompt)

                    latency = round(time.monotonic() - start_time, ndigits=2) 
                message_placeholder.write_stream(stream_output(res))
                
                st.markdown(f'<div style="text-align: right;">Latency: {latency} seconds</div>', unsafe_allow_html=True)
        
        except Exception as e:
            logging.info(f'Error in generating bot answer: {e}')
            res = st.write(stream_output("Internal Error - We're working hard to fix this as soon as possible!"))
    st.session_state.messages.append({"role": "assistant", "content": res})