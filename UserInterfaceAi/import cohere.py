import cohere

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
                                "date": {
                                    "type": "string",
                                    "format": "date",  # Specify date format
                                    "description": "The due date of the task in YYYY-MM-DD format."
                                },
                                "time": {
                                    "type": "string",
                                    "pattern": "^([01]\\d|2[0-3]):([0-5]\\d)$",
                                    "description": "The time for the task (HH:MM format, 24-hour clock).",
                                    "nullable": True
                                }
                            },
                            "required": ["name","task_type", "frequency", "times_per_day"]
                        }
                    }
                },
                "required": ["tasks"]
            }
        }
    }
]

# Cohere Chat API call with ClientV2
try:
    print("we got here")
    response = co.chat(
        model="command-r-plus",  # Use "command" or "command-nightly" if "command-r-plus" is not available
        messages=[
            {"role": "system", "content": "Always process the user's request using the 'create_tasks' tool and generate a JSON output."},
            {"role": "system", "content": "If user suggests something with a fixed day schedule it for that day in the json, if open ended feel free to give multipe days to prep"},
            {"role": "user", "content": "I want to study for my exam on friday, but I have a soccer game every saturday. I also want to go to the gym every morning"}
        ],
        tools=tools,
        temperature=0.3,  # Lower temperature for more deterministic output
    )
    print(response.message.tool_calls[0].function.arguments)
    # print(response.message)
    # print(response.message.content)
    
   

except cohere.errors.UnprocessableEntityError as e:
    print(f"Unprocessable Entity Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
