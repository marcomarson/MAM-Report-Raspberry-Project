# views.py
from __future__ import print_function # In python 2.7
import sys
from app import app
from flask import Flask, render_template, url_for, request, session, redirect
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
def trocames(x):
    if x == 'Jun':
        return 6
    elif x =='Jul':
        return 7
    elif x =='Aug':
        return 8
    elif x =='Sep':
        return 9
    elif x =='Oct':
        return 10
    elif x =='Nov':
        return 11
    elif x =='Dec':
        return 12



# # @app.route('/')
# # def index():
# #     return render_template("index.html")
#
# @app.route('/')
# def about():
#     return render_template("about.html")

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        if request.method == 'POST':
                print("Passou", file=sys.stderr)
                uri = "mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin"
                client = MongoClient(uri)
                db = client.test
                collection = db.fs.files
                cur= collection.find()
                lista=[]
                rfid1=[166,2,217,160,221]
                rfid2=[54,109,54,94,51]
                datefrom=request.form['data_12'].split('/')
                dateto=request.form['data_13'].split('/')

                apartamento= request.form['ap']
                datapre= datetime.date(int(datefrom[2]), int(datefrom[1]), int(datefrom[0]))
                datapos= datetime.date(int(dateto[2]), int(dateto[1]), int(dateto[0]))
                #print(datapre, file=sys.stderr)
                #print(datapos, file=sys.stderr)
                #if()

                for doc in cur:
                    if not apartamento:

                        if 'tempo_portao_aberto' in doc.keys() and 'rfid' in doc.keys():
                            #if()
                            if(int(doc['tempo_portao_aberto']) > 30):
                                dataprocessing= doc['horario_abertura'].split()
                                dataprocessing[1]= trocames(dataprocessing[1])
                                dataprocessada= datetime.date(int(dataprocessing[4]),dataprocessing[1], int(dataprocessing[2]))
                                print(dataprocessada, file=sys.stderr)
                                if(doc['rfid']== rfid1 and datapre<=dataprocessada<=datapos):
                                    doc['rfid']='Isabel'
                                    doc['apartamento']=12
                                    lista.append(doc)
                                elif(doc['rfid']== rfid2 and datapre<=dataprocessada<=datapos):
                                    doc['rfid']='Rogério'
                                    doc['apartamento']=30
                                    lista.append(doc)
                    else:
                        if 'tempo_portao_aberto' in doc.keys() and 'rfid' in doc.keys():
                            dataprocessing= doc['horario_abertura'].split()
                            dataprocessing[1]= trocames(dataprocessing[1])
                            dataprocessada= datetime.date(int(dataprocessing[4]),dataprocessing[1], int(dataprocessing[2]))
                            if(apartamento=='12'):

                                if(int(doc['tempo_portao_aberto']) > 30 and doc['rfid']== rfid1):
                                    doc['rfid']='Isabel'
                                    doc['apartamento']=12
                                    lista.append(doc)
                            elif(apartamento=='30'):
                                if(int(doc['tempo_portao_aberto']) > 30 and doc['rfid']== rfid2):
                                    doc['rfid']='Rogério'
                                    doc['apartamento']=30
                                    lista.append(doc)
                for x in lista:
                    print(x, file=sys.stderr)
                templatepdf=render_template('pdf.html', allvalues=lista)
                print(type(templatepdf), file=sys.stderr)
                config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
                pdfkit.from_string(templatepdf,output_path='app\\static\\pdfs\\out.pdf',configuration=config)
                print("passou", file=sys.stderr)
                return redirect(url_for('static', filename='/'.join(['pdfs', 'out.pdf'])), code=301)

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
            return redirect(url_for('login'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        if request.method == 'POST':
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['username']})

            if existing_user is None:
                hashpass = request.form['pass']
                rfid = request.form['rfid']
                users.insert({'name' : request.form['username'], 'apartamento' : hashpass, 'rfid': rfid, 'email' : request.form['email']})
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

    return redirect(url_for('index'))
