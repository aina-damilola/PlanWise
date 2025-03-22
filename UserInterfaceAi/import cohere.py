import cohere

# Correct ClientV2 import
co = cohere.ClientV2(api_key="WwNgPjpfa2Btwiv0pKw7jJzXTGLoAKbgLnaVs04l")

# Define tool as per Cohere's specs
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
                                "frequency": {
                                    "type": "string",
                                    "description": "How often the task should be done.",
                                    "enum": ["daily", "weekly", "monthly", "multiple times a day"]
                                },
                                "times_per_day": {
                                    "type": ["integer", "null"],
                                    "description": "Required if frequency is 'multiple times a day', otherwise null."
                                }
                            },
                            "required": ["name", "frequency", "times_per_day"]
                        }
                    }
                },
                "required": ["tasks"]
            }
        }
    }
]

# Cohere Chat API call with ClientV2
response = co.chat(
    model="command-r-plus",  # or latest supported model with tool use
    messages=[
        {"role": "user", "content": "Create tasks for my personal productivity system."}
    ],
    tools=tools,
    strict_tools=True
)

# Proper tool call handling with ClientV2
if response.message.tool_calls:
    for tool_call in response.message.tool_calls:
        print("Tool Call Detected:")
        print(f"  Tool Name: {tool_call['name']}")
        print(f"  Arguments: {tool_call['parameters']}")
else:
    print("No tool calls were suggested by the model.")
