from flask import Flask, request

app = Flask(__name__)

user = {
    "username" : "Sheethal",
    "password" : "abcd"
}

@app.route("/", methods=["POST"])
def hello():
    # Receive password and username
    recievedDetails = request.get_json()
    # Check if the user exists
    if user.get("username") == recievedDetails.get("username"):
        if user.get("password") == recievedDetails.get("password"):
            return "Success"
        else:
            return "Password doesnot match"
    else:
        return "User Not Found"


if __name__ == "__main__":
    app.run(debug = True, port = 6000)