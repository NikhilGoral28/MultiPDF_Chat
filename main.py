# main.py
import streamlit as st
from dotenv import load_dotenv
import os
from embedding import get_vectorstore, get_conversation_chain
from llm_helper import get_pdf_text, get_text_chunks
from htmltemplate import css, bot_template, user_template

# Load environment variables
load_dotenv()

def handle_userinput(user_q):
    response = st.session_state.conversation({"question": user_q})

    # response['chat_history'] is a list of Message objects
    chat_history = response['chat_history']  # a list of HumanMessage / AIMessage objects
    st.session_state.chat_history = chat_history

    # Display messages
    for i, message in enumerate(chat_history):
        if message.type == "human":  # or use isinstance(message, HumanMessage)
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon="📚", layout="wide")

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Inject CSS for chat styling
    st.write(css, unsafe_allow_html=True)

    # Header
    st.header("Chat with PDFs 📚")

    # User input (always active)
    user_q = st.text_input("Ask a question about your documents:")

    if user_q:
        handle_userinput(user_q)

    # Sidebar for PDF uploads
    with st.sidebar:
        st.subheader("Upload your PDFs")
        pdf_docs = st.file_uploader(
            "Upload one or more PDFs and click 'Process'",
            type=["pdf"],
            accept_multiple_files=True
        )

        if st.button("Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF!")
            else:
                with st.spinner("Processing PDFs..."):
                    # 1️⃣ Extract text from PDFs
                    raw_text = get_pdf_text(pdf_docs)

                    # 2️⃣ Split into text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # 3️⃣ Create vector store (embedding)
                    vectorstore = get_vectorstore(text_chunks)

                    # 4️⃣ Create conversational retrieval chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("Processing complete! You can now ask questions.")

if __name__ == "__main__":
    main()
