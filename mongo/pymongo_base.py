from typing import List
from pymongo import MongoClient
class PyMongo:
    client: MongoClient
    def __init__(self, db_host, db_name: str):
        self.client = MongoClient(db_host)

        self.db = self.client[db_name]
    
    def insert_one(self, collection_name: str, data: dict):
        self.db[collection_name].insert_one(data)

    def insert_list(self, collection_name: str, data: List[dict]):
        self.db[collection_name].insert_many(data)

    def get_data(self, collection_name: str, querry_dict: dict = {}, get_dict: dict = {}):
        self.db[collection_name].find(querry_dict, get_dict)
    
    def update(self, collection_name: str, querry_dict: dict, update_dict: dict):
        update_dict = {"$set": update_dict}
        self.db[collection_name].update_many(querry_dict, update_dict)