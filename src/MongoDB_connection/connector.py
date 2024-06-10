from pymongo import MongoClient
import json

class MongoDBConnector:
    def __init__(self, config:dict) -> None:
        self.config = config
        self.client = MongoClient(config["connection_string"])
        self.db = self.client[config["database"]]
        self.collection = self.db[config["collection"]]
    
    def run_query(self, query:str):
        """for exmaple query = '{"name": "John"}'"""
        result = self.collection.find(query)
        return result
    
    def run_modify(self, modify:str):
        self.collection.insert_one(json.loads(modify))