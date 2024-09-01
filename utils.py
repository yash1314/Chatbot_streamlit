import time 

# from src.model_components.model import Model
# from better_profanity import profanity


# #generate casual response when app initialize with and without file
# def casual_responses(sentence):
#     """The function generates responses based on the prompt sentiment and wording. It also restricts user and model response
#     if found inappropriate."""

#     if profanity.contains_profanity(sentence): 
#         filtered_response = random.choice(["Sorry, I cannot assist with that!",
#         "I cannot help with that. Please, Let me know how I can assist further."])

#         for word in filtered_response.split(" "):
#                 yield word + " "
#                 time.sleep(0.1)
        
#     else:
#         qa_model_output = Model.QA_model(u_input = sentence)

#         if profanity.contains_profanity(qa_model_output):
#             filtered_output = "Inappropriate response, restricting the answer. Please contiue with another question!"
#             for word in filtered_output.split(" "):
#                 yield word + " "
#                 time.sleep(0.1)

#         else:
#             for word in qa_model_output.split(" "):
#                 yield word + " "
#                 time.sleep(0.04)
        
# for streaming output letter by letter
def stream_output(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.001)
        

# formatting the prompt for model input
def message_prompt(newprompt=None, oldprompt=None):
        message = [{"role": "system", "content": "**Instructions:**\n1. Provide clear, accurate answers based on the context, including previous interactions.\n2. Use the same language as the question.\n3. Be concise but, shortish answers are better. Never omit detail.\n4. Incorporate information from previous questions and answers to provide a coherent response.\n5. If you cannot provide an answer based on the provided context, acknowledge this politely and state that you do not have enough information."}, 
                {"role": "user", "content": oldprompt[-2]['user'] if oldprompt != None else "No user message" },
                {"role": "assistant", "content": oldprompt[-2]['assistant'] if oldprompt != None else "No assistant response"},
                {"role": "user", "content": oldprompt[-1]['user'] if oldprompt != None else "No user message" },
                {"role": "assistant", "content": oldprompt[-1]['assistant'] if oldprompt != None else "No assistant response"},
                {"role": "user", "content": newprompt}]
        return message


# maintaining chat_history
chat_history = []