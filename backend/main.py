import os

from flask import Flask, jsonify, request
from agent import get_agent
from langchain_core.messages import AIMessage, HumanMessage

app = Flask(__name__)

agent = get_agent()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    conversation = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_message),
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    return {"data": conversation["messages"][-1].content}

@app.route('/', methods=['GET'])
def index():
    return f"Hello from GenAI Genesis"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))