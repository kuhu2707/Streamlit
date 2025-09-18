#Task 2: Upload a CSV file via Streamlit and display summary statistics.

import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="CSV Summary", layout="wide")
st.title(" CSV Summary Statistics")


df = pd.read_csv(r"D:\iris.csv")

# Show dataframe preview
st.subheader(" Data Preview")
st.dataframe(df.head())

# Show summary statistics
st.subheader(" Summary Statistics")
st.write(df.describe())

# Extra: Show shape and column names
st.info(f"Dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.")
st.write("Columns:", list(df.columns))
