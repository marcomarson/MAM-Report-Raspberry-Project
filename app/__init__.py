# app/__init__.py

import flask_login
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt



app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secreto'  # Change this!

app.config['MONGO_DBNAME']= 'Raspberry'
app.config['MONGO_URI']= "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"


mongo = PyMongo(app)

# Initialize the app


# Load the views
from app import views

# Load the config file
app.config.from_object('config')
