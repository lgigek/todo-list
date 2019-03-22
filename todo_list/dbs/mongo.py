import os
from pymongo import MongoClient

"""
This module creates instances to manipulate database
"""

# Gets instance of MongoDb client
client = MongoClient(os.environ.get("MONGO_CONNECTION"))

# Gets instance of a database from MongoDb
database = client[os.environ.get("MONGO_DATABASE")]

# Gets instance of a collection from database
tasks = database[os.environ.get("MONGO_TASK_COLLECTION")]
