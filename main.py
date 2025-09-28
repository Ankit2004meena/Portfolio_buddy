import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db
import google.generativeai as genai
from PIL import Image
import os

# Setup Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # or gemma-3-4b-it if you prefer
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

st.title("Portfolio Buddy 🤝")

mode = st.radio("Choose Mode:", ["PortFolio Buddy", "CHATBOT"])

if mode == "PortFolio Buddy":
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

elif mode == "CHATBOT":
    prompt = st.text_input("Enter your question:")
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Get Gemini Response"):
        response = get_gemini_response(prompt, image)
        st.subheader("Gemini's Answer:")
        st.write(response)
