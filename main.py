from Agents import ChatAgent
from Agents.tools.firebase_tools import FirebaseClient

if __name__ == "__main__": 
    agent = ChatAgent()
    agent.activate_agent()
    # fb_client = FirebaseClient()
    # print(fb_client.get_product_details("peach blush"))
