# run.py
"""This is part of a project for learning integration of MongoDB and Flask.

This is the class that starts flask and initializes the connection with Mongo using pymongo.
"""

__version__ = '0.1'
__author__ = 'Marco Marson'

from app import app




# app=Flask(__name__)
# app.secret_key = 'secreto'  # Change this!
#
# app.config['MONGO_DBNAME']= 'Raspberry'
# app.config['MONGO_URI']= "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
#
#
# db = PyMongo(app)


if __name__ == '__main__':
    app.run()
