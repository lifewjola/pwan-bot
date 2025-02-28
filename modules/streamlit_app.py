import streamlit as st
import time
from generate import answer_question
from pwan_bot_logging import append_to_sheet

st.set_page_config(page_title="PWAN-Bot", page_icon="pwan-signature-logo.png")

def extract_table_md(text):
    lines = text.splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if table_lines:
        return "\n".join(table_lines)
    return None

def main():
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        st.image("pwan_logoo.png", width=250)

    st.title("PWAN-Bot")
    with st.expander("About PWAN-Bot"):
        st.markdown(
        "<p style='text-align: center; font-size:16px; color:#2E8540;'>"
        "Welcome to the Partners West Africa Nigeria (PWAN) Bot! "
        "I'll be glad to answer all your questions about our organization and the Nigerian Criminal Justice System.</p>",
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "you.jpg" if message["role"] == "user" else "pwan-signature-logo.png"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="you.jpg"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="pwan-signature-logo.png"):
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

        st.session_state.messages.append({"role": "assistant", "content": final_text})
        try:
            append_to_sheet(prompt, final_text)
        except Exception:
            st.error("Failed to log the conversation.")
        

if __name__ == "__main__":
    main()
