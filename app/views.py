"""This is the view class of Flask.

This file is reponsible for the views in the MVC model.
"""
from __future__ import print_function  # In python 2.7
import sys,os
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
from PIL import Image
from io import StringIO
from scipy.misc import toimage
from io import BytesIO
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from bson.objectid import ObjectId

__version__ = '1.0'
__author__ = 'Marco Marson'


def trocadata(tempo):
    # dataasertrocada=tempo
    # divide=dataasertrocada.split(" ")
    # dividedata=divide[0].split("-")
    # dividehorario=divide[1].split("+")
    datacerta=str(tempo.day)+"/"+str(tempo.month)+"/"+str(tempo.year)+" às "+str(tempo.hour)+":"+str(tempo.minute)
    return datacerta


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)


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
                db=client.projeto
                fs=gridfs.GridFS(db)
                ap=request.form['ap']
                if(request.form['ap']):
                    cur= fs.find({"apartamento": ap})
                    print("passou ap", file=sys.stderr)
                else:
                    cur= fs.find()
                listafoto=[]
                x=0
                for grid_data in fs.find():
                    text = grid_data.read()
                    #print(text)
                    # Non test code
                    dataBytesIO = BytesIO(text)
                    img=Image.open(dataBytesIO)
                    img.save("C:\\Users\\Marco\\Desktop\\Python\\Python App\\Python-App-Time-Management\\app\\static\\img\\"+str(x)+".png", "PNG")
                    x=x+1
                for subdir, dirs, files in os.walk("C:\\Users\\Marco\\Desktop\\Python\\Python App\\Python-App-Time-Management\\app\\static\\img"):
                    for file in files:
                        #print os.path.join(subdir, file)
                        filepath = subdir + os.sep + file

                        if filepath.endswith(".png"):
                            listafoto.append('img\\'+file)
                            print(listafoto[0])

                return render_template("album.html", listafoto=listafoto)

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
                    data_found = list(data.find({"horario_abertura": {"$gt": datainicial}, "horario_fecha": {"$lt": datafinal}}))

                if not data_found:
                    error="Sem dados no sistema com as informações solicitadas"
                    return render_template('report.html', error=error)
                for x in data_found:
                    print (x["horario_abertura"])
                    x["horario_abertura"]=trocadata(x["horario_abertura"])
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



@app.route('/vincula')
def vincula():
    error=None
    if 'username' in session:

        return render_template('rfid.html', error=error)
    else:
        return render_template('login.html',error=error)

@app.route('/modifica')
def modifica():
    error=None
    if 'username' in session:
        users = mongo.db.users
        all_users = users.find({})
        return render_template('modify.html', error=error, people=all_users)


    else:
        return render_template('login.html',error=error)

@app.route("/modifica/<user_id>", methods=['POST', 'GET'])
def edit_users(user_id):
    error=None
    if 'username' in session:

        if request.method == 'POST':
            users = mongo.db.users

            users.update_one(
            {"_id": ObjectId(user_id)},
            {
            "$set": {
                "name":request.form['username'],
                "email":request.form['email'],
                "rfid":request.form['rfid'],
                "apartamento": request.form['ap'],
                "interfone":request.form['interfone']
            }
            }
            )
            return redirect(url_for('modifica'))
        if request.method == "GET":
            users = mongo.db.users

            specified_user=users.find_one({"_id": ObjectId(user_id)})
            print (specified_user['name'],file=sys.stderr)
            return render_template('edit.html', error=error, user=specified_user)

    else:
        return redirect(url_for('index'))

@app.route("/remove/<user_id>", methods=['GET'])
def remove_users(user_id):
    error=None
    if 'username' in session:
        if request.method == "GET":
            users = mongo.db.users

            specified_user=users.delete_one({"_id": ObjectId(user_id)})
            print (specified_user['name'],file=sys.stderr)
            return redirect(url_for('modifica'))

    else:
        return redirect(url_for('index'))

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
