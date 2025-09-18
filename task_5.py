import streamlit as st
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import pipeline
import tempfile
import os

# ---------- FILE LOADER ----------
def load_file(file):
    ext = file.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + ext) as tmp:
        tmp.write(file.getbuffer())
        tmp_path = tmp.name

    if ext == "pdf":
        loader = PyPDFLoader(tmp_path)
    else:
        st.error(f"File type {ext} not supported!")
        return []

    docs = loader.load()
    os.remove(tmp_path)
    return docs

# ---------- CHUNKING ----------
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)

# ---------- EMBEDDINGS & VECTORSTORE ----------
def build_vectorstore(splits):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return Chroma.from_documents(splits, embedding=embeddings)

# ---------- HUGGING FACE LLM ----------
@st.cache_resource
def load_hf_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

def generate_answer(llm, context, query):
    prompt = f"Answer the question using only the following context:\n\n{context}\n\nQuestion: {query}"
    result = llm(prompt, max_length=256, do_sample=True, temperature=0.3)
    return result[0]["generated_text"]

# ---------- STREAMLIT APP ----------
st.title("Chat with Your Document")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
query = st.text_input("Ask a question about your document:")

if uploaded_file and query:
    docs = load_file(uploaded_file)
    if docs:
        splits = split_docs(docs)
        vectordb = build_vectorstore(splits)
        llm = load_hf_model()

        retriever = vectordb.as_retriever(search_kwargs={"k":4})
        results = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in results])

        with st.spinner("Generating answer..."):
            answer = generate_answer(llm, context, query)

        st.subheader("Answer")
        st.write(answer)
