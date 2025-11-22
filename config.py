from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


class Settings:
    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_USERNAME: str = os.getenv("MONGO_USERNAME", "")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD", "")
    MONGO_CLUSTER: str = os.getenv("MONGO_CLUSTER", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "testdb")

    @classmethod
    def get_mongo_uri(cls) -> str:
        password_encoded = quote_plus(cls.MONGO_PASSWORD)
        return f"mongodb+srv://{cls.MONGO_USERNAME}:{password_encoded}@{cls.MONGO_HOST}?appname={cls.MONGO_CLUSTER}"
    
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "").split(",")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()


def get_mongo_client() -> MongoClient:
    uri = settings.get_mongo_uri()
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client


mongo_client = get_mongo_client()
