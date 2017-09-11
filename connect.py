# from flask import Flask
# from flask.ext.pymongo import PyMongo
# import ssl
# import flask_login
#
#
#
# app=Flask(__name__)
# app.secret_key = 'secreto'  # Change this!
#
# app.config['MONGO_DBNAME']= 'Raspberry'
# app.config['MONGO_URI']= "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
#
#
# db = PyMongo(app)
#
# login_manager = flask_login.LoginManager()
#
# login_manager.init_app(app)
