import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseClient:
    def __init__(self, service_account_path = None):
        if not service_account_path:
            service_account_path = "./firebase_key.json" 
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_product_details(self, product_name:str = None):
        """get product details from firestore
        Args:
            product_name (str): name of the product to fetch details for
        Returns:
            dict: product details if found, None otherwise
        """
        if not product_name : 
            return "product name wasn't provided to the function"
        doc = self.db.collection('products').document(product_name.lower()).get()
        if doc.exists:
            return doc.to_dict()
        else:
            return f"wasn't able to find the product named {product_name} in the database"