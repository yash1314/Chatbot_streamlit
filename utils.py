import sys, random, time
import streamlit as st
from src.exception import CustomException
from src.logging import logging


# for streaming output letter by letter
def stream_output(message):
    try: 
        for word in message.split(" "):
                yield word + " "
                time.sleep(0.07)
    except Exception as e:
          logging.error(f"Error in generating stream {e}")


# formatting the prompt for model input
@st.cache_data(show_spinner=False)
def message_prompt(newprompt=None, oldprompt=None):
        try:
                message = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions and queries.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit details.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the context, acknowledge this politely and state that you do not have enough information.\n6. Ensure all responses are suitable for all audiences and avoid adult or explicit content."}, 
                        {"role": "user", "content": oldprompt[-3]['content'] if len(oldprompt) > 2 else "No user message" },
                        {"role": "assistant", "content": oldprompt[-2]['content'] if len(oldprompt) > 2 else "No assistant response"},
                        {"role": "user", "content": newprompt}]
                return message
        except Exception as e:
              logging.info('Error in generating message prompt for model input.')
              raise CustomException(e, sys)
        

def sug_message(count:int = 1):
        suggestions = [
        "Can you help me find a recipe for dinner?",
        "What’s the weather like today?",
        "I need advice on managing stress.",
        "Tell me a fun fact about space!",
        "How do I start learning a new language?",
        "What are some good movies to watch this weekend?",
        "Help me create a workout plan.",
        "What’s trending in technology right now?",
        "Can you suggest a book to read?",
        "I’d like tips for improving my sleep.",
        "What’s the best way to save money?",
        "I need help with my resume.",
        "What are some easy crafts for kids?",
        "Can you recommend a podcast?",
        "What’s a good way to stay organized?",
        "I want to learn more about meditation.",
        "What’s the best approach to public speaking?",
        "Can you suggest some fun activities for a date?",
        "How do I improve my time management skills?",
        "What are some healthy snack ideas?",
        "Tell me about the benefits of yoga.",
        "What’s a good strategy for studying?",
        "Can you give me travel tips for Europe?",
        "What are the latest fashion trends?",
        "How do I get started with gardening?",
        "Can you help me with a math problem?",
        "What are some interesting historical events?",
        "I need ideas for a party theme.",
        "Can you help me plan a budget?",
        "What are some popular video games right now?",
        "Can you explain a complex topic simply?",
        "I’m looking for advice on starting a blog.",
        "What are some creative writing prompts?",
        "How do I make my own cleaning products?",
        "What’s the best way to network professionally?",
        "Can you give me tips for a job interview?",
        "What are the benefits of journaling?",
        "Can you recommend some board games?",
        "What should I know about cryptocurrency?",
        "How can I be more productive at work?",
        "What’s a good strategy for learning math?",
        "Can you suggest some environmental tips?",
        "What are some great outdoor activities?",
        "How do I improve my communication skills?",
        "Can you help me choose a gift for a friend?",
        "What are the signs of burnout?",
        "How do I stay motivated while studying?",
        "Can you share a quick meditation exercise?",
        "What’s the best way to approach a new hobby?" ]

        result = random.choices(suggestions, k = 3)
        return result


def on_button_click(num):
    user_message = st.session_state.message_sugg[num]
    st.session_state.user_selected_message = user_message
    st.session_state.button_clicked = 1


@st.dialog(title="Welcome to ChatNext!", width="large")
def app_info():
      st.markdown("""**Welcome! Feel free to ask anything—let’s explore together! Our chatbot aims to provide helpful responses, but remember, accuracy isn’t guaranteed. Enjoy the chat! 🚀
    :green[Enjoy exploring!]**""", unsafe_allow_html=True)
      st.markdown(" ")
      st.markdown(
    "<div style='text-align: center;'>"
    "| Made with ❤️‍🔥 by Yash Keshari |"
    "</div>",
    unsafe_allow_html=True)
      st.markdown(" ")


#