# views.py
from __future__ import print_function # In python 2.7
import sys
from app import app
from flask import Flask, render_template, url_for, request, session, redirect,send_file
from flask_pymongo import PyMongo
import pdfkit
import bcrypt
from app.__init__ import mongo
import ssl
from pymongo import MongoClient
from bson import json_util as json
from bson.objectid import ObjectId
import gridfs
import base64
import datetime
import gridfs
from PIL import Image
from io import StringIO
from scipy.misc import toimage
# def trocames(x):
#     if x == 'Jun':
#         return 6
#     elif x =='Jul':
#         return 7
#     elif x =='Aug':
#         return 8
#     elif x =='Sep':
#         return 9
#     elif x =='Oct':
#         return 10
#     elif x =='Nov':
#         return 11
#     elif x =='Dec':
#         return 12
#
#

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/photos', methods=['POST','GET'])
def photos():
    if 'username' in session:
        if request.method == 'POST':
                print("Passou", file=sys.stderr)
                datefrom=request.form['data_12'].split('/')
                dateto=request.form['data_13'].split('/')
                uri = "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
                client = MongoClient(uri)
                db = client.data
                collection = db.fs.files
                ap=request.form['ap']
                cur= collection.find({apartamento: ap})

                if not cur:
                    raise Exception("mongo file does not exist! {0}".format(filename))
                listafoto=[]
                for image in cur:
                    im=Image.open(image)
                    img_io = StringIO()
                    im.save(img_io, 'JPEG', quality=70)
                    img_io.seek(0)
                    listafoto.append(img_io)

                return render_template("album.html", listafoto,toimage)

        else:
            return render_template("photos.html")
    else:
        return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        if request.method == 'POST':
                print("Passou", file=sys.stderr)
                data = mongo.db.data
                data_found = data.find({'apartamento' : request.form['ap']})

                if data_found:
                    print("Achou")
                else:
                    return 'Não foi encontrado nada'
                # for x in lista:
                #     print(x, file=sys.stderr)
                # templatepdf=render_template('pdf.html', allvalues=lista)
                # print(type(templatepdf), file=sys.stderr)
                # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
                # pdfkit.from_string(templatepdf,output_path='app\\static\\pdfs\\out.pdf',configuration=config)
                # print("passou", file=sys.stderr)
                # return redirect(url_for('static', filename='/'.join(['pdfs', 'out.pdf'])), code=301)

        else:
            return render_template('report.html')

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        print(login_user['password'], file=sys.stderr)
        print(request.form['pass'].encode('utf-8'), file=sys.stderr)
        if  bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('register'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():

    if 'username' in session:

        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})

            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf8'), bcrypt.gensalt())
                rfid = request.form['rfid']
                users.insert({'name' : request.form['username'], 'password':hashpass,'apartamento' : request.form['ap'], 'rfid': rfid, 'email' : request.form['email']})
                return redirect(url_for('index'))

            return 'That username already exists!'

        return render_template('register.html')

    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:

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

    return redirect(url_for('index'))
