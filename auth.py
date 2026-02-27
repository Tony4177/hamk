import bcrypt
from database import users_collection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(email, password):
    if users_collection.find_one({"email": email}):
        return False
    
    hashed_pw = hash_password(password)
    users_collection.insert_one({
        "email": email,
        "password": hashed_pw
    })
    return True

def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and check_password(password, user["password"]):
        return user
    return None