from openai import OpenAI
from terminalUI import UI 
import os
from dotenv import load_dotenv
load_dotenv()
from Agent.tools.firebase_tools import FirebaseClient
from Agent.tools.schemas.firebase_tools_schemas import tools
import json

console_ui = UI()
firebase_client = FirebaseClient()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

functions = {
    "get_product_details": firebase_client.get_product_details
}

SYSTEM_PROMPT = """
You are a helpful assistant , you find product details by their names
you extract the name from the users input and u can use the function provided 'get_product_details' and give the name as a paramter then u can respond with products detail
"""

if __name__ == "__main__":

    messages = [
        {"role": "developer", "content": SYSTEM_PROMPT}
    ] 

    tool_response = False
    while True:
        # print(f"[CURRENT MSGS]{messages}")
        if not tool_response:
            prompt = console_ui._get_user_input()
            messages.append({"role": "user", "content": prompt})
            if prompt == "exit": 
                break
        response = client.responses.create(
                input=messages,
                model="openai/gpt-oss-20b",
                tools=tools
            )
        messages.extend(response.output)
        for item in response.output: 
            if item.type == "function_call": 
                if item.name in functions.keys():
                    console_ui._print_tool_call(item.name, json.loads(item.arguments))
                    kargs = json.loads(item.arguments)
                    product_details = functions[item.name](**kargs)
                    console_ui._print_tool_reponse(item.name, product_details)
                messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(product_details, default=str),
                    }
                )
                response = client.responses.create(
                    input=messages,
                    model="openai/gpt-oss-20b",
                    tools=tools
                )
                tool_response = True
                continue
            if item.type == "reasoning": 
                continue
            if item.type == "message": 
                console_ui._print_assistant_text(item.content[-1].text)
                messages.append({"role": "assistant", "content": item.content[-1].text})
                tool_response = False



