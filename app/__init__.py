"""This is the first class to start Flask.

This file is reponsible for starting the framework Flask
"""

__version__ = '1.0'
__author__ = 'Marco Marson'

import flask_login
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt



app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secretoProjeto'  # Change this!

app.config['MONGO_DBNAME']= 'projeto'
app.config['MONGO_URI']= "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
app.jinja_env.filters['zip'] = zip

mongo = PyMongo(app)

# Initialize the app


# Load the views
from app import views

# Load the config file
app.config.from_object('config')
