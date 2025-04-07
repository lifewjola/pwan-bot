import google.generativeai as genai
import streamlit as st
from retrieve import retrieve_documents 

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def answer_question(user_question: str):
    conversation = ""
    if "messages" in st.session_state:
        for message in st.session_state.messages:
            conversation += f"{message['role']}: {message['content']}\n"

    context = retrieve_documents(user_question)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )

    prompt = f"""
    Your name is PWAN Bot. You are a friendly yet formal assistant that is designed solely to answer questions related to Partners West Africa Nigeria (PWAN) and criminal justice system in Niegria. 
    Your task is to answers questions based on both the provided external context and the conversation history.
    
    Conversation history:
    {conversation}
    
    External Context:
    {context}
    
    Question: {user_question}

    NOTES: 
    1. Keep answer straight to the point
    2. If the context doesn't provide enough information to answer the question, you can gracefully admit you do not know the answer or ask for more information from the user.
    3. If a table in the context contains relevant information, you can use return the table as part of your answer to the question.
    4. Do not make it obvious that context has been provided to you or give out all the information in the context unless it is necessary to answer the question.
    """

    response = model.generate_content(prompt).text
    return response

if __name__ == "__main__":
    user_question = "What is the mission of PWAN?"
    answer = answer_question(user_question)
    print(answer)