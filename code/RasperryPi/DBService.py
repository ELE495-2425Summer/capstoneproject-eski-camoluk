from pymongo import MongoClient
from dotenv import load_dotenv
import os

class DBService:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv('URI')
        self.client = None
        self.db = None
        self.db_name = os.getenv('DB_NAME')

    def connect_db(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"Bağlantı başarılı")
        except Exception as e:
            print(f"Veritabanına bağlanırken hata oluştu: {e}")

    def update_data(self, collection_name, update_data):
        if  self.db == None:
            print("Veritabanına bağlantı yok. Önce connect_db() metodunu çağır.")
            return

        try:
            collection = self.db[collection_name]
            result = collection.update_one({}, update_data)
            print(f"{result.modified_count} belge güncellendi.")
        except Exception as e:
            print(f"Veri güncellenirken hata oluştu: {e}")
    
    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def read_document(self, collection_name):
        collection = self.db[collection_name]
        document = collection.find_one()
        return document

