from transformers import pipeline
import streamlit as st


class Model:
    
    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            model = pipeline("text-generation", model="Qwen/Qwen2-0.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            print(f"Error in loading text-to-text model: {str(e)}")


    @staticmethod
    def QA_model(message):
        answer = Model.load_t2t_model()(message, max_new_tokens = 750)
        return answer[0]['generated_text'][-1]['content']                   