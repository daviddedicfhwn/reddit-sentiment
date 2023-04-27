from contextlib import contextmanager

from pymongo import MongoClient

# Constants
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "my_database"
COLLECTION_NAME = "my_data"


@contextmanager
def mongo_connection(uri):
    client = MongoClient(uri)
    try:
        yield client
    finally:
        client.close()


def insert_data(client, database, collection, data):
    db = client[database]
    col = db[collection]
    result = col.insert_one(data)
    return result.inserted_id


def insert_many_data(client, database, collection, data_list):
    db = client[database]
    col = db[collection]
    result = col.insert_many(data_list)
    return result.inserted_ids


def get_data(client, database, collection, query):
    db = client[database]
    col = db[collection]
    result = col.find(query)
    return list(result)
