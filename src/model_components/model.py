from transformers import pipeline
import streamlit as st
import sys

from src.logging import logging
from gradio_client import Client


class Model:
    
    @st.cache_resource(show_spinner=False)
    def load_t2t_model():
        try:
            model = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", use_fast=True)
            return model
        except Exception as e:
            logging.info('Error in model model loading')
            
    
    @staticmethod
    def model_generate(message):
        if client := Client("Qwen/Qwen2.5-72B-Instruct"):
            try:
                result = client.predict(query = message, history= [],
                                        system = "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions and queries.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit details.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the context, acknowledge this politely and state that you do not have enough information.\n6. Ensure all responses are suitable for all audiences and avoid adult or explicit content.",
                                        api_name = "/model_chat")
                return result[1][0][-1]
            except Exception as e:
                logging.info('Error in gradio model Inferencing.')

        else:
            try: 
                answer = Model.load_t2t_model()(message, max_new_tokens = 750)
                return answer[0]['generated_text'][-1]['content']                   
            except Exception as e:
                logging.info('Error in model answer generation')