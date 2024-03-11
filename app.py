import streamlit as st
import requests
import pyperclip
import time
import main
import os

def copy_to_clipboard():
        pyperclip.copy(st.session_state.result)
        success=st.success("Result copied to clipboard!")
        time.sleep(3)
        success.empty()

def displayResult():
        st.write(f"Answer ({st.session_state.time_taken}s):")
        st.write(st.session_state.result)
        col1, col2 = st.columns(2)
        # Use a persistent "Copy" button
        copy_button=col1.button("Copy to Clipboard")
        save_button=col2.button("Click to Save")
        if copy_button and st.session_state.result:
            copy_to_clipboard()
        
        if save_button:
             save_answers()
        with st.expander("Reference Documents "):
             for docs in st.session_state.source_documents:
                  st.write(docs)
def save_answers():
    filename = f"QA_Pairs.txt"
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Question: {st.session_state.query}\n")
        file.write(f"Answer: {st.session_state.result}\n\n\n")

def makeUI():
    st.set_page_config(page_title="NCC-AI")
    parent_folder_path = './source_documents'
    folder_names = [f for f in os.listdir(parent_folder_path) if os.path.isdir(os.path.join(parent_folder_path, f)) and not f.startswith('.')]
    st.header("NCC-AI👨‍💻")
    st.sidebar.title("Documents Available")
    for folder_name in folder_names:
        st.sidebar.write("- "+folder_name)
    st.sidebar.markdown('[Extract Report](https://36a2ce3eb7b0e6d-dot-us-central1.notebooks.googleusercontent.com/lab/tree/NCC_AI/QA_Pairs.txt) ⬇️')
    if "result" not in st.session_state:
        st.session_state.result=None
    if "time_taken" not in st.session_state:
        st.session_state.time_taken=None
    if "source_documents" not in st.session_state:
         st.session_state.source_documents=None
    if "page_content" not in st.session_state:
         st.session_state.page_content=None
    if "query" not in st.session_state:
         st.session_state.query=None
    st.write("Welcome to Nokia Converged Charging!")
    query = st.text_input("How may I help you?", key="input_box")
    st.session_state.query=query
    if st.button("Submit"):
        with st.spinner("Generating..."):
            response = requests.post("http://127.0.0.1:5001/ask", json={"question": "In reference to Nokia Converged Charging reply in detail for "+query})
        if response.status_code == 200:
            st.session_state.result = response.json()["answer"]
            st.session_state.time_taken=response.json()["time_taken"]
            st.session_state.source_documents=response.json()["source_documents"]
            st.session_state.page_content=response.json()["page_content"]
        else:
            st.write("Error:", response.json()["error"])
    
    if st.session_state.result:
        displayResult()


if __name__ == "__main__":
    makeUI()