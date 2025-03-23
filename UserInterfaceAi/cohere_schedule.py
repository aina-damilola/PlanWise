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

def map_tasks_to_calendar(input_json):
    mapped_tasks = {"tasks": []}
    modified = json.loads(input_json)
    for task in modified["tasks"]:
        title = task.get("name")

        frequency = task.get("frequency")
        if frequency is None:
            frequency = "one time"

        start_time = task.get("time")  # 24-hour format (HH:MM)
        if start_time is None:
            start_time = "00:00:00"
        # Handle One-Time Events
        if frequency == "one time":
            date = task.get('date')
            if date == None:
                date = task.get('start_date')
            if date == None:
                date = "2025-03-22"

            event = {
                "title": title,
                "start": f"{date}T{start_time}"
            }
            mapped_tasks["tasks"].append(event)

        # Handle Recurring Events
        elif frequency in ["daily", "weekly", "monthly", "yearly"]:
            date = task.get('start_date')
            if date == None:
                date = "2025-03-22"
            rrule = {
                "freq": frequency,
                "dtstart": f"{date}T{start_time}"
            }
            
            # Check for additional recurrence rules
            if frequency == "weekly":
                rrule["byweekday"] = "mo"  # Assuming Monday; update based on data
            elif frequency == "monthly":
                rrule["bymonthday"] = 1  # Assuming the first of the month
            elif frequency == "yearly":
                rrule["bymonth"] = 1  # Assuming January
                rrule["bymonthday"] = 1  # Assuming 1st of January

            # Optional stop conditions
            if "until" in task:
                rrule["until"] = f"{task['until']}T23:59:59"
            elif "count" in task:
                rrule["count"] = task["count"]

            mapped_tasks["tasks"].append({"title": title, "rrule": rrule})

    return json.dumps(mapped_tasks, indent=4)

# Initialize Cohere ClientV2
co = cohere.ClientV2(api_key="WwNgPjpfa2Btwiv0pKw7jJzXTGLoAKbgLnaVs04l")  # Replace with your actual API key

# Corrected tool definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_tasks",
            "description": "Create a list of tasks with their frequencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "description": "A list of tasks to create.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the task."
                                },
                                "task_type": {
                                    "type": "string",
                                    "description": "Indicates if the task is a 'fixed_event', 'recurring_event', or an 'open_task' that has a deadline but no specific time.",
                                    "enum": ["fixed_event", "recurring_event", "open_task"]
                                },
                                "frequency": {
                                    "type": "string",
                                    "description": "How often the task should be done.",
                                    "enum": ["daily", "weekly", "monthly", "multiple times a day","one time"]
                                },
                                "times_per_day": {
                                    "type": "integer",
                                    "description": "Required if frequency is 'multiple times a day', otherwise null.",
                                    "nullable": True
                                },
                                "start_date": {
                                    "type": "string",
                                    "format": "date",  # Specify date format
                                    "description": "The start date of the task in YYYY-MM-DD format."
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date",  # Specify date format
                                    "description": "The deadline of the task in YYYY-MM-DD format."
                                },
                                "time": {
                                    "type": "string",
                                    "pattern": "^([01]\\d|2[0-3]):([0-5]\\d)$",
                                    "description": "The time for the task (HH:MM format, 24-hour clock).",
                                    "nullable": True
                                }
                            },
                            "required": ["name","task_type", "frequency", "times_per_day", "start_date"]
                        }
                    }
                },
                "required": ["tasks"]
            }
        }
    }
]

def generate(user_message):
# Cohere Chat API call with ClientV2
    try:
      
        response = co.chat(
            model="command-r-plus",  # Use "command" or "command-nightly" if "command-r-plus" is not available
            messages=[
                {"role": "system", "content": "Always process the user's request using the 'create_tasks' tool and generate a JSON output."},
                {"role": "system", "content": "If user suggests something with a fixed day schedule it for that day in the json, if open ended feel free to give multipe days to prep"},
                {"role": "system", "content": "Also factor in the fact that today is March 22nd 2025"},
                {"role": "user", "content": user_message}
            ],
            tools=tools,
            temperature=0.4,  # Lower temperature for more deterministic output
        )

        #print(response.message.tool_calls[0].function.arguments)
        results = response.message.tool_calls[0].function.arguments
        #print(results)
        
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

    results = map_tasks_to_calendar(results)

    return jsonify({"response": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

