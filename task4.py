#Task 4: Add session state to your app to maintain chat history.


import streamlit as st
from transformers import pipeline


generator = pipeline("text-generation", model="distilgpt2")

st.title("Text Generation App with Chat History")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []


user_input = st.text_area("Enter your prompt:", "Once upon a time")

if st.button("Generate"):
    with st.spinner("Generating..."):
        output = generator(user_input, max_length=100, num_return_sequences=1)
        response = output[0]['generated_text']

        # Save conversation in session state
        st.session_state.history.append({"prompt": user_input, "response": response})

# Display chat history
if st.session_state.history:
    st.write("## Chat History")
    for i, chat in enumerate(st.session_state.history, 1):
        st.write(f"**Prompt {i}:** {chat['prompt']}")
        st.success(f"**Response {i}:** {chat['response']}")
