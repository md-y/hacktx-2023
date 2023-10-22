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

#dict format
testUserData = {
  "assets": [
    {
      "asset_name": "Asset Name",
      "function_type": "exponential",
      "initial_value": "0",
      "min_max_value": 0,
      "r": 0.5,
      "starting_date": "10/21/2023"
    }
  ],
  "bills": [
    {
      "payment_amount": 0,
      "payment_date": "10/21/2023"
    }
  ],
  "checking_account_balance": 0,
  "checking_account_reward": 0,
  "credit_card_balance": 0,
  "credit_card_rewards": 0,
  "deposits": [
    {
      "account": "checkings",
      "amount": 0,
      "date": "10/21/2023"
    }
  ],
  "monthly_bills": [
    {
      "amount": 0
    }
  ],
  "savings_account_balance": 0,
  "savings_account_rewards": 0,
  "uid": "",
  "withdrawls": [
    {
      "account": "checkings",
      "amount": 0,
      "date": "10/21/2023"
    }
  ]
}




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
def get_user():
    #Add this line to all things
    uid = check_auth()
    if uid == "":
        return {"Error": "Error"}, 400
    
    try:
        #for test just get and print a user
        users = usersRef.where("uid", "==", uid).stream()
        user = next(users).to_dict()
        del user['uid']
        return user
    
    except Exception as error:
        print(error)
        return {"Error": "Error"}, 400
    
@api.route('/user', methods=['POST', 'PUT'])
@cross_origin()
def post_user():
    #Add this line to all things
    uid = check_auth()
    if uid == "":
        return {"Error": "Error"}, 400
    
    try:
        #check if user already exists
        users = usersRef.where("uid", "==", uid).stream()
        user = request.json
        user['uid'] = uid

        if testUserData.keys() != user.keys():
            return {"Error": "Invalid Object"}, 400
        
        if users:
            userDocId = next(users).id
            usersRef.document(userDocId).set(user)
        else:
            usersRef.document().set(user)

        #print(json.dumps(user, indent=2))
        return user
    except Exception as error:
        print(error)
        return {"Error": "Error"}, 400
    

    
if __name__ == '__main__':
    api.run(port=2000) 