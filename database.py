import psycopg2
import uuid
import os
import hashlib
import psycopg2.extras
from constants import *

class Database:
    def __init__(self) -> None:

        self.connection = psycopg2.connect(
                host=DBHOST,
                database=DBNAME,
                user=DBUSER,
                password=DBPASSWORD
                )

        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def compare(self, credentials):
        # Receive cred from frontend
        # Compare with the copy in database to validate

        # Retrive from the database
        sql = "SELECT userid, email, password FROM users WHERE email = %s"
        self.cursor.execute(sql, (credentials.get("email"), ))
        user = dict(self.cursor.fetchone())

        # compare passwords
        # 128 characters - first 64 is the salt and next 64 is the hashed password
        salt = bytes.fromhex(user.get("password")[:64])
        receivedPassword = hashlib.pbkdf2_hmac('sha256', credentials.get("password").encode('utf-8'), salt, 100000)

        if receivedPassword.hex() == user.get("password")[64:]:
            return user.get("userid")
        return None
    
    def validate(self, userId):
        # Check if user exists
        sql = "SELECT userid FROM users WHERE userId = %s"
        self.cursor.execute(sql, (userId, ))
        user = self.cursor.fetchone() # returns 1 or 0 elements
        if user:
            return True
        return False


    
    def storeUser(self, user):
        try:
            # Generate random user Id
            userId = str(uuid.uuid4())

            # Hashing password

            # This generates 32 random bytes
            salt = os.urandom(32)

            # hashed will be 32 bytes
            hashed = hashlib.pbkdf2_hmac('sha256', user.get("password").encode('utf-8'), salt, 100000)
            password = salt.hex() + hashed.hex()
            
            # Create and run sql
            sql = """
            INSERT INTO users (userid, email, password, age, name) VALUES 
            (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (userId, user.get("email"), password, int(user.get("age")), user.get("name")))
        except Exception as e:
            print(str(e))
            self.connection.rollback()
            return None, str(e)
        else:
            print("User Added")
            self.connection.commit()
            return userId, None

    def getUser(self, userId):
        sql = "SELECT userid AS id, email, name, age FROM users WHERE userId = %s"
        self.cursor.execute(sql, (userId, ))
        user = self.cursor.fetchone()
        return dict(user)
    
    def getAllUser(self):
        sql = "SELECT userid AS id, email, name, age FROM users"
        self.cursor.execute(sql)
        user = list(self.cursor.fetchall())
        # (("id", "name", "age", "email"), ("id", "name", "age", "email"), ("id", "name", "age", "email"), )
        for i in range(len(user)):
            user[i] = dict(user[i])
        return user
        # return [dict(i) for i in user]
    
    def __repr__(self) -> str:
        return "I'm a database connector object"


if __name__ == "__main__":
    database = Database()

    # userId = database.storeUser(
        # {
        #     "name" : "Shrirama",
        #     "password" : "Password",
        #     "age" : "21",
        #     "email" : "shrirama@domain.com"
        # }
    # )
    # if userId:
    print(dict(database.getUser("18b761eb-7f99-456a-9cad-49ae80920aa0")))
