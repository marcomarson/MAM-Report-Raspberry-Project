"""This is the view class of Flask.

This file is reponsible for the views in the MVC model.
"""
from __future__ import print_function  # In python 2.7
import sys
from app import app
from flask import Flask, render_template, url_for, request, session, redirect, send_file
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

__version__ = '1.0'
__author__ = 'Marco Marson'

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/photos', methods=['POST','GET'])
def photos():
    error=None
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
                    Error= " Não possui fotos no sistema com durante esse período"
                    return render_template("photos.html", error=error)
                listafoto=[]
                for image in cur:
                    im=Image.open(image)
                    img_io = StringIO()
                    im.save(img_io, 'JPEG', quality=70)
                    img_io.seek(0)
                    listafoto.append(img_io)

                return render_template("album.html", listafoto,toimage)

        else:
            return render_template("photos.html", error=error)
    else:
        return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    error=None
    if 'username' in session:
        if request.method == 'POST':
                print("Passou", file=sys.stderr)
                data = mongo.db.data
                datafrom=request.form['data_12']
                datafrom=datafrom+" 22:00:00"
                datato=request.form['data_13']
                datato=datato+" 22:00:00"
                datainicial=datetime.datetime.strptime(datafrom,"%d/%m/%Y %H:%M:%S")
                datainicial=datainicial.isoformat()
                datainicial=datetime.datetime.strptime(datainicial, "%Y-%m-%dT%H:%M:%S")
                datafinal=datetime.datetime.strptime(datato,"%d/%m/%Y %H:%M:%S")
                datafinal = datafinal.isoformat()
                datafinal=datetime.datetime.strptime(datafinal, "%Y-%m-%dT%H:%M:%S")
                datafinal=datafinal.replace(tzinfo=None)
                print(datafinal)
                if(request.form['ap']):
                    print("apzitcho")
                    data_found = list(data.find({'apartamento' : request.form['ap'], "horario_abertura": {"$gte": datainicial}}))
                else:
                    data_found = list(data.find({"horario_abertura": {"$gt": datainicial}}))


                for x in data_found:
                    print (x["horario_abertura"])
                templatepdf=render_template('pdf.html', allvalues=data_found)
                print(type(templatepdf), file=sys.stderr)
                config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
                pdfkit.from_string(templatepdf,output_path='app\\static\\pdfs\\out.pdf',configuration=config)
                print("passou", file=sys.stderr)
                return redirect(url_for('static', filename='/'.join(['pdfs', 'out.pdf'])), code=301)

        else:
            return render_template('report.html', error=error)

    return render_template('login.html', error=error)

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
    error="Erro no Login, senha ou login incorretos."
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    error=None
    if 'username' in session:

        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})
            existing_rfid= users.find_one({'rfid' : request.form['rfid']})
            existing_email=users.find_one({'email' : request.form['email']})
            existing_interfone=users.find_one({'interfone' : request.form['interfone']})

            if existing_user is None and existing_rfid is None and existing_email is None and existing_interfone is None :
                #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf8'), bcrypt.gensalt())
                rfid = request.form['rfid']
                users.insert({'name' : request.form['username'],'interfone':request.form['interfone'], 'apartamento' : request.form['ap'], 'rfid': rfid, 'email' : request.form['email']})
                return redirect(url_for('index'))

            error='Alguma informação já está sendo utilizada em outro usuario!'
            return render_template('register.html', error=error)

        return render_template('register.html', error=error)

    else:
        return render_template('login.html',error=error)


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
