from os import getenv
from typing import Dict, Iterable, Iterator
from random import randrange

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    def __init__(self):
        # Load environmental variables
        load_dotenv()

        # Create a connection to the MongoDB server
        # client = MongoClient(getenv("DB_URL"), tlsCAFile=where())['Database']
        # client = MongoClient('localhost', 27017)
        self.client = MongoClient(getenv("DB_URL"), tlsCAFile=where())

        # Select the database
        self.db = self.client['Database']

        # Select the collection
        self.collection = self.db['Monsters']

    # def __init__(self, collection: str):
    #     self.collection = self.database[collection]
    #
    def create_one(self, record: Dict = None) -> bool:
        if record is None:
            record = Monster().to_dict()
        return self.collection.insert_one(record).acknowledged

    def read_one(self, query: Dict = None) -> Dict:
        if query is None:
            pipeline = [
                {'$sample': {'size': 1}}
            ]
            record = list(self.collection.aggregate(pipeline))
        return self.collection.find_one(query, {"_id": False})

    def update_one(self, query: Dict, update: Dict) -> bool:
        return self.collection.update_one(query, {"$set": update}).acknowledged

    def delete_one(self, query: Dict) -> bool:
        return self.collection.delete_one(query).acknowledged

    def create_many(self, records: Iterable[Dict]) -> bool:
        return self.collection.insert_many(records).acknowledged

    def read_many(self, query: Dict) -> Iterator[Dict]:
        return self.collection.find(query, {"_id": False})

    def update_many(self, query: Dict, update: Dict) -> bool:
        return self.collection.update_many(query, {"$set": update}).acknowledged

    def delete_many(self, query: Dict) -> bool:
        return self.collection.delete_many(query).acknowledged

    def seed(self, amount):
        records = [Monster().to_dict() for _ in range(amount)]
        return self.create_many(records)

    def reset(self):
        records = {}
        return self.delete_many(records)

    def count(self) -> int:
        # client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
        # db = client['Database']
        # collection = db['Monsters']
        # Use the count_documents method to get the count of documents in the collection
        query = {}
        count = self.collection.count_documents(query)  # {} means no filter, so it counts all documents
        print(f'There are {count} documents in the collection.')
        return count

    def dataframe(self) -> DataFrame:
        query = {}
        df = DataFrame(list(self.read_many(query)))
        return df

    def html_table(self) -> str:
        return 'here\'s the table'

if __name__ == '__main__':
    #db = Database("Collection")
    db = Database()
    #db.create_many({"Value": randrange(1, 100)} for _ in range(10))
    #print(DataFrame(db.read_many({})))
    print(db.client)
    #databases = db.client.list_database_names()
    #print(databases)

    # use list_collection_names method to get a list of all collection names
    collections = db.client.list_collection_names()

    # print the collections
    for collection in collections:
        print(collection)