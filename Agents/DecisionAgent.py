from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
from dotenv import load_dotenv

class DecisionAgent: 
    def __init__(self):
        self.client = TypeSafeClient(model="jev-latest")    

    def match_label(self, user_input:str, choices:list[str]): 
        response_choice = Choice(
            instructions="which is the best match for this product name, if there is no match u must chose 'no match found'",
            criteria=choices
        )
        response = self.client.system_one(
        state=user_input,
        questions={
            "matching_label":response_choice})

        print("[JEV RESPONSE]", response)
        return response.choices["matching_label"].choice
    

