#Task 1: Create a "Hello AI" Streamlit app with user input and text output.

import streamlit as st 
 
st.title("Hello AI")

name = st.text_input("Enter your name:")
message = st.text_area("Write a message for AI:")

if st.button("say hello"):
    if name:
        st.success(f"Hello,{name}")
    else:
        st.success("Hello, AI")
        
    if message:
        st.write("**AI says**" , message)