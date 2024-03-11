#!/usr/bin/env python3
import time
from flask import Flask, request, jsonify
import main

app = Flask(__name__)
qa = None


@app.route('/ask', methods=['POST'])
def ask_question():
    global qa
    if qa is None:
        qa=main.main() 
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.json
    if 'question' not in data:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    question = data['question']
    # Get the answer from the chain
    start = time.time()
    res = qa(question)
    answer, docs = res['result'], res['source_documents']
    end = time.time()
    source_documents=[]
    page_content=[]
    time_taken=end-start
    for document in docs:
        source_documents.append(document.metadata["source"])
        page_content.append(document.page_content)

    return jsonify({"answer": answer,"time_taken":round(time_taken,2),"source_documents":source_documents,"page_content":page_content})


if __name__ == "__main__":
    qa=main.main() 
