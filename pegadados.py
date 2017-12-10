
# Pegando todos os dados do MongoDB.
import os
from pymongo import MongoClient
import gridfs
import datetime
import time
def savelogrfid(rfid,data):
    client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
    db=client.projeto
    db.rfid.insert({'rfid' : rfid, 'data' : data})

def gravaInformacoesRFID(rfid,data):
    path = 'rfidlog.txt'
    txt_rfid = open(path,'a+')
    instr = "{0};{1};\n".format(rfid, data)
    txt_rfid.write(instr)


data= time.strftime("%d %b %Y %H:%M:%S")
rfid1=[166,2,217,160,221]
rfid2=[54,109,54,94,51]
str1 = ''.join(str(e)+"-" for e in rfid1)

gravaInformacoesRFID(str1,data)


path = 'rfidlog.txt'
f = open(path,'r')
if f.mode == 'r':
    fl =f.readlines()
    for line in fl:
        x=line.split(";")
        x[0]=x[0].replace("[", "")
        x[0]=x[0].replace("]", "")
        rfid=x[0].split("-")
        rfid=rfid[:-1]
        rfid=list(map(int,rfid)) ##py 2 would be map(int,rfid)
        data=datetime.datetime.strptime(x[1],"%d %b %Y %H:%M:%S")
        savelogrfid(rfid,data)
    f.close()
open(path, 'w').close()
