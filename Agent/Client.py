from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from Agent.tools.firebase_tools import FirebaseClient
from Agent.tools.schemas.firebase_tools_schemas import tools
import json


firebase_client = FirebaseClient()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

functions = {
    "get_product_details": FirebaseClient.get_product_details
}

SYSTEM_PROMPT = """
You are a helpful assistant , you find product details by their names
you extract the name from the users input and u can use the function provided 'get_product_details' and give the name as a paramter then u can respond with products detail
"""

if __name__ == "__main__":
    prompt = input("[YOU]:")
    messages = [
        {"role": "developer", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ] 
    while True:
        response = client.responses.create(
                input=messages,
                model="openai/gpt-oss-20b",
                tools=tools
            )
        print(response.output)
        for item in response.output : 
            if item.type == "function_call": 
                print(f"[TOOL CALL {item.name}]")
                if item.name in functions.keys():
                    print(f"[RUNING TOOL{item.name}]")
                    product_name = json.loads(item.arguments)["product_name"]
                    product_details = functions[item.name]
                    print(f"[TOOL OUTPUT]{product_details}")
                messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": product_details,
                    }
                )
                continue
        print(f"[ASSISTANT] {response.text}")
        break


