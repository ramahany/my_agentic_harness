from Agents import ChatAgent
from db_manage.FireStoreManager import FireStoreManager
from Agents.tools.firebase_tools import FirebaseClient

if __name__ == "__main__": 
    fb = FireStoreManager()
    # agent = ChatAgent(products = fb.get_products_choices())
    # agent.activate_agent()
    fb_client = FirebaseClient(products=fb.get_products_choices())
    print(fb_client.get_product_details("Amber Oud"))
