from transformers import pipeline
import streamlit as st
import sys

from src.exception import CustomException
from src.logging import logging


class Model:
    
    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            model = pipeline("text-generation", model="Qwen/Qwen2-1.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            logging.info('Error in model model loading')
            CustomException(e, sys)


    @staticmethod
    def QA_model(message):
        try: 
            answer = Model.load_t2t_model()(message, max_new_tokens = 750)
            return answer[0]['generated_text'][-1]['content']                   
        except Exception as e:
            logging.info('Error in model answer generation')
            CustomException(e, sys)