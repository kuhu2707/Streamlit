import streamlit as st
from transformers import pipeline

# No token needed for public models
generator = pipeline("text-generation", model="distilgpt2")

st.title("Text Generation App")

user_input = st.text_area("Enter your prompt:", "Once upon a time")

if st.button("Generate"):
    with st.spinner("Generating..."):
        output = generator(user_input, max_length=100, num_return_sequences=1)
        st.write("### Generated Text:")
        st.success(output[0]['generated_text'])
