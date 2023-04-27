from pymongo import MongoClient

from config import DATABASE_NAME, MONGODB_URI

client, db = None, None


def insert_many_data(collection, data_list):
    if data_list is None or len(data_list) == 0:
        return None

    col = db[collection]
    result = col.insert_many(data_list)
    return result.inserted_ids


def get_data(collection, query):
    col = db[collection]
    result = col.find(query)
    return list(result)


def connect_to_db():
    global client, db
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]


def close_db_connection():
    global client
    client.close()
