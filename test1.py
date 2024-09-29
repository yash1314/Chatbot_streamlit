import random, time, sys
import streamlit as st 
from streamlit import _bottom
from better_profanity import profanity
from src.logging import logging

from utils import message_prompt, stream_output, sug_message, app_info, on_button_click
from src.model_components.model import Model
from PIL import Image
from streamlit_lottie import st_lottie_spinner
from artifact.animations.lottie_animation import animation2


# # page setup
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# bot and user chat alignment
with open ('design.css') as source:
    st.markdown(f"<style>{source.read()}</style>",unsafe_allow_html=True)


# # design elements layouts
st.markdown('<style>div.block-container{padding-top:0.8rem;}</style>', unsafe_allow_html=True)

st.header(f"*:orange[Chat]Next*! 💬")
# st.markdown("")
# # st.markdown("""**Welcome! Feel free to ask anything—let’s explore together! Our chatbot aims to provide helpful responses, but remember, accuracy isn’t guaranteed. Enjoy the chat! 🚀
# #     :green[Enjoy exploring!]**""", unsafe_allow_html=True)

if st.button('App info'):
    app_info()

st.markdown(
    "<div style='text-align: left;'>"
    "<a href='https://www.linkedin.com/in/yash907'>LinkedIn</a> | Made with ❤️‍🔥 by Yash Keshari"
    "</div>",
    unsafe_allow_html=True)
st.markdown(" ")

# images and lottie animations
bot_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/chatbot.png"
user_img = "https://raw.githubusercontent.com/yash1314/Chatbot_streamlit/refs/heads/main/artifact/man.png"
lottie_url = animation2()



# # initializing session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "message_sugg" not in st.session_state:
    st.session_state.message_sugg = sug_message(3)

if "user_selected_message" not in st.session_state:
    st.session_state.user_selected_message = ""

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = 0

if "first_message" not in st.session_state:
    st.session_state.first_message = 0  #can only contain 0 or 1 


for message in st.session_state.messages:
    if message['role'] == 'user':
        with st.chat_message(message["role"], avatar=user_img):
            st.markdown(message["content"])
    elif message['role'] == 'assistant':
        with st.chat_message(message["role"], avatar=bot_img):
            st.markdown(message["content"])


#app suggestions
if st.session_state.button_clicked == 0:
    with _bottom:
        col1, col2, col3, col4, col5 = st.columns(5)    
        with col2:
            if st.button(label=st.session_state.message_sugg[0], use_container_width=True, key="1button", on_click=on_button_click(0)):
                pass
                
        with col3:
            if st.button(label=st.session_state.message_sugg[1], use_container_width=True, key="2button", on_click=on_button_click(1)):
                pass
                
        with col4:
            if st.button(label=st.session_state.message_sugg[2], use_container_width=True, key="3button", on_click=on_button_click(2)):
                pass

suggestion_user_message = st.session_state.user_selected_message

#chat elements
if st.session_state.button_clicked == 1:
    prompt = st.session_state.user_selected_message

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
#                 # with st.spinner("Thinking..."):
                with st_lottie_spinner(lottie_url,height=35, width=60):
                    start_time = time.monotonic()
                    res = Model.model_generate(message=prompt)

                    latency = round(time.monotonic() - start_time, ndigits=2) 
                message_placeholder.write_stream(stream_output(res))
                
                st.markdown(f'<div style="text-align: right;">Latency: {latency} seconds</div>', unsafe_allow_html=True)
        
        except Exception as e:
            logging.info(f'Error in generating bot answer: {e}')
            res = st.write(stream_output("Internal Error - We're working hard to fix this as soon as possible!"))
    st.session_state.messages.append({"role": "assistant", "content": res})

else:
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
#                     # with st.spinner("Thinking..."):
                    with st_lottie_spinner(lottie_url,height=35, width=60):
                        start_time = time.monotonic()
                        res = Model.model_generate(message=prompt)

                        latency = round(time.monotonic() - start_time, ndigits=2) 
                    message_placeholder.write_stream(stream_output(res))
                    
                    st.markdown(f'<div style="text-align: right;">Latency: {latency} seconds</div>', unsafe_allow_html=True)
            
            except Exception as e:
                logging.info(f'Error in generating bot answer: {e}')
                res = st.write(stream_output("Internal Error - We're working hard to fix this as soon as possible!"))
        st.session_state.messages.append({"role": "assistant", "content": res}) 


