from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Allow all origins & credentials

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def generate(user_message):
# Cohere Chat API call with ClientV2
    try:
      
        response = co.chat(
            model="command-r-plus",  # Use "command" or "command-nightly" if "command-r-plus" is not available
            messages=[
                {"role": "system", "content": "Always process the user's request using the 'create_tasks' tool and generate a JSON output."},
                {"role": "system", "content": "If user suggests something with a fixed day schedule it for that day in the json, if open ended feel free to give multipe days to prep"},
                {"role": "user", "content": user_message}
            ],
            tools=tools,
            temperature=0.4,  # Lower temperature for more deterministic output
        )
        results = response.message.tool_calls[0].function.arguments
        results = json.dumps(map_tasks_to_calendar(results), indent=4)
        # print(response.message)
        # print(response.message.content)
        return results
        

    except cohere.errors.UnprocessableEntityError as e:
        print(f"Unprocessable Entity Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



@app.route("/generate", methods=["POST"])
def generate_endpoint():
    data = request.json  # Receive data from the frontend
    user_message = data.get("text")  # Extract user input text

    results = generate(user_message)

    return jsonify({"response": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
