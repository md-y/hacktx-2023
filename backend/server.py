#Authenticate and connect withe firestore
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("./authenticationKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#for test just get and print a user
docs = db.collection("Users").stream()
for doc in docs:
    print(doc.to_dict())


#FLASK SERVER
from flask import Flask, json, request
from flask_cors import CORS, cross_origin

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

#Checks if user is authenticated
def check_auth():
    token = request.headers.get("Authtoken", None)
    if token == None:
        return False
    decoded_token = auth.verify_id_token(token)    
    uid = decoded_token['uid']    
    return True

@api.route('/', methods=['GET'])
@cross_origin()
def endpoint():
    #Add this line to all things
    if not check_auth():
        return {"error": "error"}, 400
    

    try:
        return {"test": "this is a test"}
    except Exception as error:
        print(error)
        return {"Error": "Error"}, 400
    
if __name__ == '__main__':
    api.run(port=2000) 