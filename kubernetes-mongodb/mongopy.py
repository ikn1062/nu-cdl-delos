from pymongo import MongoClient
import os

MONGO_SERVER: os.getenv('MONGO_SERVER')
MONGO_USER: os.getenv('MONGO_USERNAME')
MONGO_PASS: os.getenv('MONGO_PASS')
print(MONGO_SERVER)
connect = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_SERVER}:27017/admin?ssl=true"
client = MongoClient(connect)
print("CONNECTED!")
client.close()
