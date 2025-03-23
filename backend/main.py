import os
import base64

from io import BytesIO
from flask import Flask, jsonify, request
from flask_cors import CORS
from agent import get_agent
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image

app = Flask(__name__)
CORS(app)

agent = get_agent()

@app.route('/api/chat', methods=['POST', 'OPTIONS']) 
def chat():
    if request.method == "OPTIONS":
        return cors_response()
    
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    conversation = agent.invoke(
        {
            "messages": [
                HumanMessage(content=f"{user_message}; The user id of the calling user is ian123"),
            ],
        },
        config={"configurable": {"thread_id": "1"}}
    )

    return cors_response({"data": conversation["messages"][-1].content})

@app.route('/api/image_chat', methods=['POST', 'OPTIONS'])
def image_chat():
    if request.method == "OPTIONS":
        return cors_response()

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Get the image and prompt from the request
    image_file = request.files['image']
    prompt = request.form['prompt']
    
    try:
        # Process the image
        image = Image.open(image_file)
        
        # Convert PIL Image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_bytes = buffered.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Create multimodal message with media type
        multimodal_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "media",
                    "mime_type": "image/jpeg",
                    "data": image_base64
                }
            ]
        )
        
        # Use your existing agent to process the multimodal input
        conversation = agent.invoke(
            {
                "messages": [multimodal_message],
            },
            config={"configurable": {"thread_id": "1"}}
        )
        
        # Return the generated text
        return cors_response({"data": conversation["messages"][-1].content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/image', methods=['POST', 'OPTIONS'])
def image():
    if request.method == "OPTIONS":
        return cors_response()

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Get the image and prompt from the request
    image_file = request.files['image']
    
    try:
        # Process the image
        image = Image.open(image_file)
        
        # Convert PIL Image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_bytes = buffered.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Create multimodal message with media type
        multimodal_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "Can you extract the transactions of this receipt that I just made in the image provided?"
                },
                {
                    "type": "media",
                    "mime_type": "image/jpeg",
                    "data": image_base64
                }
            ]
        )
        
        # Use your existing agent to process the multimodal input
        conversation = agent.invoke(
            {
                "messages": [multimodal_message],
            },
            config={"configurable": {"thread_id": "1"}}
        )
        
        # Return the generated text
        return cors_response({"data": conversation["messages"][-1].content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return f"Hello from GenAI Genesis"

@app.route('/api/test', methods=['POST', 'OPTIONS']) 
def test():
    if request.method == "OPTIONS":  
        return cors_response()
    return cors_response({"data": "hello from the other side."})

def cors_response(response_data={}):
    """✅ Helper function to add CORS headers to responses"""
    response = jsonify(response_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
