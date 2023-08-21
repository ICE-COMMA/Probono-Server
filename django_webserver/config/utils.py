from pymongo import MongoClient
from django.contrib.sessions.backends.db import SessionStore as DBStore
from datetime import datetime, timedelta

def get_db_handle(db_name, host, port):
    client = MongoClient(host=host, port=int(port))
    db_handle = client[db_name]
    return db_handle, client

def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]

connect_host = 'mongodb+srv://andyc707:tzlZgVWMs1wFvzDH@prototypeversion.sxa69i7.mongodb.net/'
db_handle, mongo_client = get_db_handle('Prototype', connect_host, '27017')
#conn = get_collection_handle(db_handle, 'Prototype')

session_collection = get_collection_handle(db_handle, 'session')

class SessionStore(DBStore):
    def load(self):
        try:
            session_data = session_collection.find_one({'session_key': self.session_key})
            return self.decode(session_data['session_data'])
        except:
            self.create()
            return {}

    def exists(self, session_key):
        if session_collection.find_one({'session_key': session_key}):
            return True
        return False
#####
    def save(self, must_create=False):
        session_data = {
        'session_key': self._get_or_create_session_key(),
        'session_data': self.encode(self._get_session(no_load=must_create)),
        'expire_date': self._get_session_expiry_date()
        }
        if must_create:
            if self.exists(self.session_key):
                raise CreateError() # 세션 키가 이미 존재하므로 생성할 수 없습니다.
            session_collection.insert_one(session_data)
        else:
            session_collection.update_one({'session_key': self.session_key}, {'$set': session_data}, upsert=True)
    
    ######
    # def save(self, must_create=False):
    #     session_data = {
    #         'session_key': self._get_or_create_session_key(),
    #         'session_data': self.encode(self._get_session(no_load=must_create)),
    #         'expire_date': self._get_session_expiry_date()
    #     }
    #     if must_create:
    #         print('asdfdsfsfslklnklnkjlnlknklnklnklnklnklnkl')
    #         session_collection.insert_one(session_data)
    #     else:
    #         session_collection.update_one({'session_key': self.session_key}, {'$set': session_data})

    def delete(self, session_key=None):
        if not session_key:
            session_key = self._get_or_create_session_key()
        session_collection.delete_one({'session_key': session_key})

    def _get_session_expiry_date(self):
        expiry_duration = timedelta(hours=1)
        return datetime.now() + expiry_duration