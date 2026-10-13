import streamlit as st

from rag import ask_question


st.set_page_config(
    page_title="Ollama RAG",
    page_icon="📚"
)


st.title("📚 Ollama RAG Document Assistant")

st.write(
    "Ask questions about your documents."
)


question = st.text_input(
    "Ask your question"
)


if question:

    with st.spinner("Thinking..."):

        answer = ask_question(question)

    st.subheader("Answer")

    st.write(answer)