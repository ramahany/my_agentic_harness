from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from Agents.tools.firebase_tools import FirebaseClient
from data.prompts.assistant_prompts import SYSTEM_PROMPT
from Agents.tools.schemas.firebase_tools_schemas import tools
import json
from helpers.TTS import TTS
from terminalUI import UI

class ChatAgent: 

    def __init__(self):
        self.UI = UI()
        self.firebase_client = FirebaseClient()
        self.model = "openai/gpt-oss-20b"
        self.client = OpenAI(
                api_key=os.environ.get("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1",
            )
        self.functions = {"get_product_details": self.firebase_client.get_product_details}
        self.messages = [
                {"role": "developer", "content": SYSTEM_PROMPT}
            ]
        self.TTS = TTS()

    def get_response(self):
        return self.client.responses.create(
                input=self.messages,
                model=self.model,
                tools=tools
            )
    
    def add_message_with_role(self, role:str, content:str): 
        self.messages.append({"role": role, "content": content})

    def activate_agent(self): 
        tool_response = False
        while True:
            if not tool_response:
                prompt = self.UI._get_user_input()
                self.add_message_with_role(role = "user", content =  prompt)
                if prompt == "exit": 
                    break
            response = self.get_response()
            self.messages.extend(response.output)
            for item in response.output: 
                if item.type == "function_call": 
                    if item.name in self.functions.keys():
                        self.UI._print_tool_call(item.name, json.loads(item.arguments))
                        kargs = json.loads(item.arguments)
                        product_details = self.functions[item.name](**kargs)
                        self.UI._print_tool_reponse(item.name, product_details)
                    self.messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(product_details, default=str),
                        }
                    )
                    response = self.get_response()
                    tool_response = True
                    continue
                if item.type == "message": 
                    self.UI._print_assistant_text(item.content[-1].text)
                    self.add_message_with_role(role = "assistant", content = item.content[-1].text)
                    self.TTS.play_audio_from_text(item.content[-1].text)
                    tool_response = False
    
    
    
    

    


    
