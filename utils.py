from src.model_components.model import Model
import streamlit as st
import time, random
from better_profanity import profanity


# generate casual response when app initialize with and without file
def casual_responses(sentence):
    """The function generates responses based on the prompt sentiment and wording. It also restricts user and model response
    if found inappropriate."""

    if profanity.contains_profanity(sentence): 
        filtered_response = random.choice(
        ["Sorry, I cannot assist you with that!",
        "I'm here to assist you. If you have any concerns or issues, please let me know, and I'll do my best to address them.",
        "I cannot help you with that. Please, Let me know how I can assist further."])

        for word in filtered_response.split(" "):
                yield word + " "
                time.sleep(0.1)
        
    else:
        qa_model_output = Model.QA_model(u_input = sentence)

        if profanity.contains_profanity(qa_model_output):
            filtered_output = "Inappropriate output, therefore restricting the answer. Please ask another question !"
            for word in filtered_output.split(" "):
                yield word + " "
                time.sleep(0.1)

        else:
            for word in qa_model_output.split(" "):
                yield word + " "
                time.sleep(0.04)