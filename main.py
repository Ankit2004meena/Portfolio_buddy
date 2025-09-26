import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

st.title("Portfolio Buddy 🤝")
page_bg = """
<style>

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Create Knowledgebase"):
    create_vector_db()
    st.success("✅ Knowledgebase created successfully!")

if question := st.chat_input("Ask a question..."):
    chain = get_qa_chain()
    response = chain(question)

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": response["result"]})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
