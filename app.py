import streamlit as st
import requests


def makeUI():
    st.set_page_config(page_title="NCC-AI")
    st.header("NCC-AI")
    query=st.text_input("Ask a question...")
    
    if query:
        response = requests.post("http://localhost:5001/ask", json={"question": "In reference to Nokia Converged Charging "+query})
        if response.status_code == 200:
            result = response.json()["answer"]
            time_taken=response.json()["time_taken"]
            st.write(f"Answer ({time_taken}s):")
            st.write(result)
        else:
            st.write("Error:", response.json()["error"])

if __name__ == "__main__":
    makeUI()
