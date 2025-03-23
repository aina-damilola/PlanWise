import os
import requests
from flask import Flask, jsonify, request
from agent import get_agent
from langchain_core.messages import AIMessage, HumanMessage

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    response = requests.post(
        'https://plan-974351744512.us-central1.run.app/api/chat',
        json={"message": user_message}
    )

    if response.status_code == 200:
        # Assuming the response contains a message or useful data
        return jsonify({"response": response.json()})
    else:
        return jsonify({"error": "Failed to get a valid response from external API"}), 500

@app.route('/', methods=['GET'])
def index():
    return f"Hello from GenAI Genesis"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))