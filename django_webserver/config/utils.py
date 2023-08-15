from pymongo import MongoClient

def get_db_handle(db_name, host, port):
    client = MongoClient(host=host, port=int(port))
    db_handle = client[db_name]
    return db_handle, client

def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]

connect_host = 'mongodb+srv://andyc707:tzlZgVWMs1wFvzDH@prototypeversion.sxa69i7.mongodb.net/'
db_handle, mongo_client = get_db_handle('Prototype', connect_host, '27017')

#conn = get_collection_handle(db_handle, 'Prototype')