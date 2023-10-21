#Authenticate and connect withe firestore
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("./authenticationKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#for test just get and print a user
docs = db.collection("Users").stream()
for doc in docs:
    print(doc.to_dict())


#FLASK SERVER
from flask import Flask, json, request
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

@api.route('/endpoint', methods=['GET'])
def endpoint():
    try:
        return {"test": "this is a test"}
    except Exception as error:
        print(error)
        return "Error", 400
    
if __name__ == '__main__':
    api.run(port=2000) 