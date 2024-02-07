import streamlit as st
import requests
import pyperclip
import time

def copy_to_clipboard():
        pyperclip.copy(st.session_state.result)
        success=st.success("Result copied to clipboard!")
        time.sleep(3)
        success.empty()

def displayResult():
        st.write(f"Answer ({st.session_state.time_taken}s):")
        st.write(st.session_state.result)
            # Use a persistent "Copy" button
        if st.button("Copy to Clipboard") and st.session_state.result:
            copy_to_clipboard()
        with st.expander("Reference Documents "):
             for docs in st.session_state.source_documents:
                  st.write(docs)
        if st.button("Click to Save"):
             save_answers()
def save_answers():
    filename = f"QA_Pairs.txt"
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Question: {st.session_state.query}\n")
        file.write(f"Answer: {st.session_state.result}\n\n\n")

def makeUI():
    st.set_page_config(page_title="NCC-AI")
    st.header("NCC-AI👨‍💻")
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
    query=st.text_input("Ask a question...")
    st.session_state.query=query
    
    if st.button("Submit"):
        with st.spinner("Generating..."):
            response = requests.post("http://localhost:5001/ask", json={"question": "In reference to Nokia Converged Charging "+query})
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
