import time
from flask import Flask, request, jsonify
import main


app = Flask(__name__)
chat_engine = None


@app.route('/ask', methods=['POST'])
def ask_question():
    global chat_engine
    if chat_engine is None:
        chat_engine=main.main() 
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.json
    if 'question' not in data:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    query = data['question']
    # Get the answer from the chain
    start = time.time()
    response = chat_engine.chat(query)
    answer = str(response)
    end = time.time()
    time_taken=end-start
    

    return jsonify({"answer": answer,"time_taken":round(time_taken,2)})


if __name__ == "__main__":
    chat_engine=main.main() 