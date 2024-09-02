import time, sys, random
import streamlit as st


# for streaming output letter by letter
def stream_output(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.03)
        

# formatting the prompt for model input
@st.cache_data(show_spinner=False)
def message_prompt(newprompt=None, oldprompt=None):
        message = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit details.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the context, acknowledge this politely and state that you do not have enough information."}, 
                {"role": "user", "content": oldprompt[-2]['user'] if oldprompt != None else "No user message" },
                {"role": "assistant", "content": oldprompt[-2]['assistant'] if oldprompt != None else "No assistant response"},
                {"role": "user", "content": oldprompt[-1]['user'] if oldprompt != None else "No user message" },
                {"role": "assistant", "content": oldprompt[-1]['assistant'] if oldprompt != None else "No assistant response"},
                {"role": "user", "content": newprompt}]
        return message


# maintaining chat_history
chat_history = []
# print(sys.getsizeof(chat_history))