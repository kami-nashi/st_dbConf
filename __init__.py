import configparser as conf
from flask import jsonify
import pymysql

def baseConfig():
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig

def dbconnect(sql,vTUP=None):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql, vTUP)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables
