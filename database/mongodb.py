from pymongo import MongoClient
from config import settings


# Cria o cliente MongoDB usando a URI do config.py
client = MongoClient(settings.get_mongo_uri())

# Seleciona o banco de dados
db = client[settings.MONGO_DB_NAME]


class MongoDB:
    '''
    Classe para interagir com o banco de dados MongoDB.
    '''
    @staticmethod
    def get_collection(collection_name):
        return db[collection_name]
    
