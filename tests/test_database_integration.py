import unittest

from src.database import MongoDBClient
from tests.test_constants import TEST_DATABASE_NAME, TEST_COLLECTION_NAME


class TestDatabaseIntegration(unittest.TestCase):
    """
    Unit Test class for the MongoDBClient integration.

    Methods:
        setUp: Initializes a MongoDBClient with the necessary configurations.
        tearDown: Cleans up the MongoDBClient and drops the test database.
        test_insert_many_data: Tests the insertion of multiple data items into a collection and validates the operation.
        test_get_data: Tests the retrieval of data from a collection and validates the operation.
        test_update_data_by_id: Tests the update operation for a specific document by its id and validates the operation.
    """
    def setUp(self):
        self.client = MongoDBClient(database_name=TEST_DATABASE_NAME)

    def tearDown(self):
        with self.client:
            self.client.drop_database(TEST_DATABASE_NAME)

    def test_insert_many_data(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]

        with self.client:
            inserted_ids = self.client.insert_many_data("test_collection", data_list)
            self.assertIsNotNone(inserted_ids)
            self.assertEqual(len(inserted_ids), 2)

    def test_get_data(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]

        with self.client:
            self.client.insert_many_data("test_collection", data_list)
            result = self.client.get_data("test_collection", {"name": "John"})
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "John")

    def test_update_data_by_id(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]

        with self.client:
            inserted_ids = self.client.insert_many_data(TEST_COLLECTION_NAME, data_list)
            doc_id = inserted_ids[0]
            self.client.update_data_by_id(TEST_COLLECTION_NAME, doc_id, {"age": 35})
            updated_data = self.client.get_data(TEST_COLLECTION_NAME, {"_id": doc_id})
            self.assertEqual(updated_data[0]["age"], 35)


if __name__ == "__main__":
    unittest.main()
