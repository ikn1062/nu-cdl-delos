from pymongo import MongoClient, errors
import os

MONGO_SERVER = os.getenv('MONGO_SERVER')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USERNAME')
MONGO_PASS = os.getenv('MONGO_PASS')


def mongo_connect():
    """
    Function that connects to the mongo database and establishes a client connection
    :return: mongo client
    """
    try:
        mongodb_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_SERVER}:{MONGO_PORT}"
        client = MongoClient(mongodb_uri)
        print("CONNECTED!")
        return client
    except errors.ConnectionFailure as e:
        print(f"[Error] Could not connect, error: {e}")
        client.close()
        return None


def insert(collection, record):
    """
    Reads the record and inserts it into the mongodb
    :param collection: Collection to insert record into
    :param record: Adding the record
    :return: None
    """
    if type(record) == list:
        collection.insert_many(record)
    else:
        collection.insert_one(record)


if __name__ == "__main__":
    client = mongo_connect()
    if client:
        mydb = client["k8s_database"]
        mycol = mydb["k8s_records"]

        record1 = {"name": "Steve", "programming_language": "C"}
        record2 = {"name": "Frank", "programming_language": "C++"}
        record34 = [{"name": "John", "programming_language": "Python"},
                    {"name": "Kevin", "programming_language": "Java"}]

        insert(mycol, record1)
        insert(mycol, record2)

        for r in mycol.find():
            print(r)

        insert(mycol, record34)

        for r in mycol.find():
            print(r)

        client.close()
    else:
        pass

