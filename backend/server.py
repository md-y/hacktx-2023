#Authenticate and connect withe firestore
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("./authenticationKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
usersRef = db.collection("Users")

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
        return ""
    decoded_token = auth.verify_id_token(token)    
    uid = decoded_token['uid']
    return uid

@api.route('/user', methods=['GET'])
@cross_origin()
def user():
    #Add this line to all things
    uid = check_auth()
    if uid == "":
        return {"Error": "Error"}, 400
    
    try:
        #for test just get and print a user
        users = usersRef.where("uid", "==", uid).stream()
        user = next(users).to_dict()
        return user
    
    except Exception as error:
        print(error)
        return {"Error": "Error"}, 400
    
if __name__ == '__main__':
    api.run(port=2000) 