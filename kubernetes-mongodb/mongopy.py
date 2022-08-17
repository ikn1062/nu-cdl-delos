from pymongo import MongoClient
import os

MONGO_SERVER = os.getenv('MONGO_SERVER')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USERNAME')
MONGO_PASS = os.getenv('MONGO_PASS')
connect = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_SERVER}:{MONGO_PORT}"
client = MongoClient(connect)
print("CONNECTED!")
print(client.list_database_names())
client.close()
