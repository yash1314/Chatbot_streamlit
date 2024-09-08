import time, sys, random
import streamlit as st
from src.exception import CustomException
from src.logging import logging


# for streaming output letter by letter
def stream_output(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.05)


# formatting the prompt for model input
@st.cache_data(show_spinner=False)
def message_prompt(newprompt=None, oldprompt=None):
        try:
                message = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions and queries.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit details.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the context, acknowledge this politely and state that you do not have enough information.\n6. Ensure all responses are suitable for all audiences and avoid adult or explicit content."}, 
                        {"role": "user", "content": oldprompt[-5]['content'] if len(oldprompt) > 3 else "No user message" },
                        {"role": "assistant", "content": oldprompt[-4]['content'] if len(oldprompt) > 3 else "No assistant response"},
                        {"role": "user", "content": oldprompt[-3]['content'] if len(oldprompt) > 2 else "No user message" },
                        {"role": "assistant", "content": oldprompt[-2]['content'] if len(oldprompt) > 2 else "No assistant response"},
                        {"role": "user", "content": newprompt}]
                return message
        except Exception as e:
              logging.info('Error in generating message prompt for model input.')
              CustomException(e, sys)