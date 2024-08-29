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
    def QA_model(u_input):
        messages = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers.\n2. Limit answers to 201 tokens while excluding query input tokens.\n3. Use the same language as the question.\n4.Shortish answers are better. But don't omit detail."},
                    {"role": "user", "content": u_input}]
        
        output = Model.load_t2t_model()(messages, max_new_tokens = 151+len(u_input.split(" ")))
        return output[0]['generated_text'][2]['content']
            
            
            
                   