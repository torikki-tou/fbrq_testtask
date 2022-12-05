from pymongo import MongoClient

from src.core import settings


class MongoClientGenerator:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_CONNECTION_STRING)

    def __call__(self) -> MongoClient:
        return self.client

    def __del__(self) -> None:
        self.client.close()


get_mongo_client = MongoClientGenerator()
