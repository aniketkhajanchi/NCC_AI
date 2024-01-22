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

def makeUI():
    if "result" not in st.session_state:
        st.session_state.result=None
    if "time_taken" not in st.session_state:
        st.session_state.time_taken=None
    st.set_page_config(page_title="NCC-AI")
    st.header("NCC-AI")
    query=st.text_input("Ask a question...")
    
    if st.button("Submit"):
        with st.spinner("Generating..."):
            response = requests.post("http://localhost:5001/ask", json={"question": "In reference to Nokia Converged Charging "+query})
        if response.status_code == 200:
            result = response.json()["answer"]
            time_taken=response.json()["time_taken"]
            st.session_state.result=result
            st.session_state.time_taken=time_taken
        else:
            st.write("Error:", response.json()["error"])
    
    if st.session_state.result:
        displayResult()

    # Use a persistent "Copy" button
    if st.button("Copy to Clipboard") and st.session_state.result:
        copy_to_clipboard()


if __name__ == "__main__":
    makeUI()
