import unittest

from src.database import (
    insert_many_data,
    get_data,
    update_data_by_id, connect_to_db, close_db_connection,
)
from tests.test_constants import TEST_DATABASE_NAME, TEST_COLLECTION_NAME


class TestDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.client, self.db = connect_to_db(TEST_DATABASE_NAME)

    def tearDown(self):
        self.client.drop_database(TEST_DATABASE_NAME)
        close_db_connection()

    def test_insert_many_data(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]
        inserted_ids = insert_many_data("test_collection", data_list)
        self.assertIsNotNone(inserted_ids)
        self.assertEqual(len(inserted_ids), 2)

    def test_get_data(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]
        insert_many_data("test_collection", data_list)
        result = get_data("test_collection", {"name": "John"})
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John")

    def test_update_data_by_id(self):
        data_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 28},
        ]
        inserted_ids = insert_many_data(TEST_COLLECTION_NAME, data_list)
        doc_id = inserted_ids[0]
        update_data_by_id(TEST_COLLECTION_NAME, doc_id, {"age": 35})
        updated_data = get_data(TEST_COLLECTION_NAME, {"_id": doc_id})
        self.assertEqual(updated_data[0]["age"], 35)


if __name__ == "__main__":
    unittest.main()
