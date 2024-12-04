from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime

connection_string = "mongodb://localhost:27017/"

def save_chat(data:dict):
    data['timestamp'] = datetime.now() 
    with MongoClient(connection_string) as client:
        client['uet_demo']['chat'].insert_one(data)

def fetch_data(userid:str):
    with MongoClient(connection_string) as client:
        return list(client['uet_demo']['chat'].find({'user_id': userid}).sort("timestamp", ASCENDING))