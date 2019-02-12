import os
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_CONNECTION"))
database = client[os.environ.get("MONGO_DATABASE")]
tasks = database[os.environ.get("MONGO_TASK_COLLECTION")]
