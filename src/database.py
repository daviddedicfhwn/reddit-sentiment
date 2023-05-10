from pymongo import MongoClient

from src.config import DATABASE_NAME, MONGODB_URI


class MongoDBClient:
    """
    A MongoDB client class that provides methods to interact with the MongoDB database.
    """

    def __init__(self):
        """
        Initialize the connection to the MongoDB database.
        """
        self.client = None
        self.db = None

    def insert_many_data(self, collection, data_list):
        """
        Insert multiple documents into the specified collection.

        :param collection: The name of the collection to insert data into.
        :param data_list: A list of dictionaries containing the data to be inserted.
        :return: A list of ObjectIDs of the inserted documents.
        """
        if data_list is None or len(data_list) == 0:
            return None

        col = self.db[collection]
        result = col.insert_many(data_list)
        return result.inserted_ids

    def get_data(self, collection, query):
        """
        Retrieve documents from the specified collection based on the given query.

        :param collection: The name of the collection to query data from.
        :param query: A dictionary representing the MongoDB query.
        :return: A list of documents matching the query.
        """
        col = self.db[collection]
        result = col.find(query)
        return list(result)

    def update_data_by_id(self, collection, doc_id, data):
        """
        Update a document in the specified collection by its ID with the given data.

        :param collection: The name of the collection to update data in.
        :param doc_id: The ObjectID of the document to update.
        :param data: A dictionary containing the data to update.
        """
        col = self.db[collection]
        col.update_one({'_id': doc_id}, {'$set': data}, upsert=False)

    def connect_to_db(self, database_name):
        """
        Establish a connection to the MongoDB database.

        :param database_name: The name of the database to connect to.
        """
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[database_name]

    def close_db_connection(self):
        """
        Close the connection to the MongoDB database.
        """
        self.client.close()

    def __enter__(self):
        """
        Return the MongoDBClient object when the MongoDBClient object is used as a context manager.
        """
        self.connect_to_db(DATABASE_NAME)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection to the MongoDB database when the MongoDBClient object is used as a context manager.
        """
        self.close_db_connection()

    def __del__(self):
        """
        Close the connection to the MongoDB database when the MongoDBClient object is deleted.
        """
        self.close_db_connection()
