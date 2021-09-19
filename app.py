from flask import Flask, request, jsonify
from database import Database
import datetime
import jwt
from functools import wraps
from constants import SECRET

app = Flask(__name__)


database = Database()

# CRUD
# Create - POST
# Read - GET
# Update - PUT
# Delete - DELETE

def validateToken(f):
    # Validate token
    # If token is valid then send the data else send forbidden/unauthorised
    @wraps(f)
    def wrapper(*args, **kwargs):
        # recieve token in headers
        token = request.headers.get('Authorization')
        if token:
            try:
                # decode token
                data = jwt.decode(token, SECRET, algorithms=['HS256'])
                # if the user exists in database
                if database.validate(data.get("userId")):
                    # Decorated function call
                    return f(*args, **kwargs)
                    
                return jsonify({"result" : "User doesnot exist", "status" : "Unauthorised"}), 401

            except Exception as e:
                # Invalid or expired token
                return jsonify({"result" : str(e), "status" : "Internal server error"}), 500
        
        # If no token
        return jsonify({"result" : "", "status" : "Unauthorised"}), 401
    return wrapper


# Login route
@app.route("/login", methods=["POST"])
def login():
    # Receive email and password
    credentials = request.get_json()

    # Check if the user exists
    userid = database.compare(credentials)
    if userid:
        # generate jwt
        payload = {
            "userId" : userid,
            # Expiration
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=50)
        }
        token = jwt.encode(payload, SECRET, algorithm='HS256').decode("ascii")
        return jsonify({"result" : token, "status" : "Success"}), 200
    return jsonify({"result" : "User Not found", "status" : "Unauthorized"}), 401


@app.route("/user", methods=["POST"])
@validateToken
def addNewUser():
    # Receive user details
    user = request.get_json()

    # Check if the user exists
    userid, error = database.storeUser(user)
    if userid:
        return jsonify({"result" : userid, "status" : "Success"}), 201
    return jsonify({"result" : error, "status" : "Internal server error"}), 500

@app.route("/user/<string:id>", methods=["GET"])
@validateToken
def getUser(id):
    # Check if the user exists
    user = database.getUser(id)
    if user:
        return jsonify({"result" : user, "status" : "Success"}), 200
    return jsonify({"result" : "No user found", "status" : "Failure"}), 200

@app.route("/user", methods=["GET"])
@validateToken
def getAllUser():
    # Get all users from database
    user = database.getAllUser()
    if user:
        return jsonify({"result" : user, "status" : "Success"}), 200
    return jsonify({"result" : "No user found", "status" : "Failure"}), 200

if __name__ == "__main__":
    app.run(debug = True, port = 6000)