# views.py

from app import app
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from app.__init__ import mongo

# # @app.route('/')
# # def index():
# #     return render_template("index.html")
#
# @app.route('/')
# def about():
#     return render_template("about.html")

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})

            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                users.insert({'name' : request.form['username'], 'password' : hashpass})
                session['username'] = request.form['username']
                return redirect(url_for('index'))

            return 'That username already exists!'

        return render_template('register.html')

    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/report', methods=['POST', 'GET'])
def report():
    # if request.method == 'POST':
        # users = mongo.db.users
        # existing_user = users.find_one({'name' : request.form['username']})
        #
        # if existing_user is None:
        #     hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        #     users.insert({'name' : request.form['username'], 'password' : hashpass})
        #     session['username'] = request.form['username']
        #     return redirect(url_for('index'))
        #
        # return 'That username already exists!'

    return render_template('report.html')
