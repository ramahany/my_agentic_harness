import firebase_admin
from firebase_admin import credentials, firestore
from ..DecisionAgent import DecisionAgent

class FirebaseClient:
    def __init__(self, service_account_path = None):
        if not service_account_path:
            service_account_path = "./firebase_key.json" 
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.decision_agent = DecisionAgent()
        self.available_products = self.get_products_choices()

    
    def get_products_choices(self) -> list[str]:
        items =self.db.collection('products').stream()
        choices = {"no match found": "if no match from other options"}
        for item in items : 
            choices[item.id] = item.to_dict()["description"]
        return choices

    def check_match_product(self, item_name): 
        return self.decision_agent.match_label(item_name, self.available_products)


    def get_product_details(self, product_name:str = None):
        """get product details from firestore
        Args:
            product_name (str): name of the product to fetch details for
        Returns:
            dict: product details if found, None otherwise
        """
        if not product_name : 
            return "product name wasn't provided to the function"
        matching_product = self.check_match_product(product_name)
        if matching_product == "no match found": 
            return "no match found after match search"
        doc = self.db.collection('products').document(matching_product).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return f"wasn't able to find the product named {product_name} in the database"

        def is_in_stock(self, item_name): 
            pass