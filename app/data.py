from os import getenv
from typing import Dict, Iterable, Iterator
from random import randrange

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

# TODO: Noticed a bug while making the html_table: the Example Monster Updated,
#  Copper Drake doesn't have a timestamp. Has NaN instead.

''' 
The Database class is an interface between a Pymongo database
hosted on Atlas https://cloud.mongodb.com/ using MongoClient.
The interface supports CRUD, and has business logic functions as well.
There are also functions to seed the database, reset it, wrap the data 
in a dataframe, and create an html table from the dataframe.
'''
class Database:
    '''
    The init function creates a connection to the Atlas hosted database
    using a environment file string. And also sets class variables for
    the database 'db' and the Monster collection 'collection'
    '''
    def __init__(self):
        # Load environmental variables
        load_dotenv()

        # Create a connection to the MongoDB server
        self.client = MongoClient(getenv("DB_URL"), tlsCAFile=where())

        # Select the database
        self.db = self.client['Database']

        # Select the collection
        self.collection = self.db['Monsters']

    '''
    CRUD operation create_one creates a single Monster in the database.
    If no input Monster record is given, it creates a random Monster.
    It uses the pymongo insert_one method: https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.insert_one
    It returns a bool as type pymongo.results.InsertOneResult 
    '''
    def create_one(self, record: Dict = None) -> bool:
        if record is None:
            record = Monster().to_dict()
        return self.collection.insert_one(record).acknowledged

    '''
    CRUD operation read_one reads a single record matching the query
    If no query is given, then it returns the first record.
    In the MongoDB context, passing None as the query to find_one will 
    return the first document in the collection without any filter, 
    excluding the _id field.
    '''
    # TODO: Make the if block usable where this function returns a random record.
    #   Right now it returns the first record every time.
    def read_one(self, query: Dict = None) -> Dict:
        # if query is None:
        #     pipeline = [
        #         {'$sample': {'size': 1}}
        #     ]
        #     record = list(self.collection.aggregate(pipeline))
        return self.collection.find_one(query, {"_id": False})

    '''
    CRUD operation update_one takes a query and an update dictionary
    and updates the the first matching record to the query with the new info.
    The $set operator replaces the value of the field or creates it if is does
    not exist.
    Returns a pymongo.results.UpdateResult which has properties: acknowledged, 
    matched_count (num of docs matching), modified_count (num of docs modified),
    raw_result(raw doc returned from server), upserted_id (id of upserted doc)
    '''
    # TODO: Should we change these CRUD operations to return the full objects?
    #   Right now they only return the bool 'acknowledged' and drop the other
    #   object info - like counts of updated records, etc.
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
        df = self.dataframe()
        html_table = df.to_html(border=1, classes='dataframe', index=True)
        return html_table
        # return 'here\'s the table'

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