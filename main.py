import openai
import json
import requests
import os
from dotenv import load_dotenv
from get_weather_data import get_current_location,get_rain_precipitation, get_uv_radiation
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def run_conversation(user_input):
    
    messages = [{"role": "user", "content": user_input}]
    functions = [
        {
            "name": "get_rain_precipitation",
            "description": "Get the current precipitation in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city, e.g. San Francisco",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_uv_radiation",
            "description": "Get the current uv radiation in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city, e.g. San Francisco",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_wind_speed",
            "description": "Get the current wind speed in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city, e.g. San Francisco",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_wind_direction",
            "description": "Get the current wind direction in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city, e.g. San Francisco",
                    },
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto", 
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_rain_precipitation": get_rain_precipitation,
            "get_uv_radiation": get_uv_radiation
        }  
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location")
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  
        return second_response


def chat(user_input):
    response = run_conversation(user_input)
    return response["choices"][0]["message"]["content"]

user_input = input("Type your question: ")
assistant_response = chat(user_input)
print(assistant_response)






