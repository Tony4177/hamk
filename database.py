from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["medicine_app"]

users_collection = db["users"]
medicines_collection = db["medicines"]