import firebase_admin
from firebase_admin import credentials, firestore

class FireStoreManager:
    def __init__(self, service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_product_details(self, product_name): 
        doc = self.db.collection('products').document(product_name).get()
        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
