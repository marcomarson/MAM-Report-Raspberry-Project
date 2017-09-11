
# Pegando todos os dados do MongoDB.

import ssl
from pymongo import MongoClient
from bson import json_util as json
from bson.objectid import ObjectId
import gridfs
import base64
uri = "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
client = MongoClient(uri)
db = client.test
collection = db.fs.files
cur= collection.find()

for doc in cur:
    print(doc)  # or do something with the document
