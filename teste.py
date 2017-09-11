


#Esse algoritmo consegue reconstruir a imagem que foi salva no mongoDB utilizando GRIDFS.
#Algorithm to test my conexion with MongoDB Atlas, and to try to extract some information from it

import ssl
from pymongo import MongoClient
from bson import json_util as json
from bson.objectid import ObjectId
import gridfs
import base64
uri = "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
client = MongoClient(uri)
db = client['test']
collection = db['fs.files']
fs=gridfs.GridFS(db)
a=fs.get(ObjectId('59474eb174fece046d7c7f56'))
a=a.read()
b=a
a= base64.b64decode(a)
print (a)
print (type(a))
print (len(a))
print (type(a[3]))


# Write to a file to show conversion worked
with open('test.jpg', 'wb') as f_output:
    f_output.write(b)

# encoded_img_file=base64.b64encode(a.read())
#
# print(encoded_img_file)
# Image2=Image.open(encoded_img_file)
# image2.show()
