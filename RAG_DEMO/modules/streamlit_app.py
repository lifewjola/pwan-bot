import streamlit as st
import time
from generate import answer_question

st.set_page_config("PWAN-Bot", page_icon="pwan-signature-logo.png")

def extract_table_md(text):
    lines = text.splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if table_lines:
        return "\n".join(table_lines)
    return None

def main():
    _, _, logo = st.columns(3)
    logo.image("logo_pwan.png", width=300,)
    st.title("PWAN-Bot")
    st.expander("Welcome to the Partners West Africa Nigeria (PWAN) Bot! I'll be glad to answer all your questions about our organization and Nigerian Criminal Justice System.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me a question"):
        st.session_state.messages.append({"role": "You", "content": prompt})
        with st.chat_message("You", avatar="you.jpg"):
            st.markdown(prompt)

        with st.chat_message("pwan-bot", avatar="pwan-signature-logo.png"):
            response_text = answer_question(prompt)
            table_md = extract_table_md(response_text)
            if table_md:
                with st.spinner("Thinking..."):
                    st.markdown(response_text)
            else:
                placeholder = st.empty()
                accumulated = ""
                for word in response_text.split():
                    accumulated += word + " "
                    placeholder.markdown(accumulated)
                    time.sleep(0.05)
            final_text = response_text  
        st.session_state.messages.append({"role": "pwan-bot", "content": final_text})

if __name__ == "__main__":
    main()
