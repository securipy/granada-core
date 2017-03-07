#!/usr/bin/python3
#-*-coding:utf-8-*-
#- sessions class

#- Copyright (C) 2014 GoldraK & Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

# WebSite: http://adminserver.org/
# Email: contacto@adminserver.org
# Facebook: https://www.facebook.com/pages/Admin-Server/795147837179555?fref=ts
# Twitter: https://twitter.com/4dminserver

import sys, os, datetime, requests, json, base64 
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
#sys.path.append('model')

class Session(object):

    def __init__(self):
        self.APIURL = ""
        self.username = ""
        self.password = ""
        self.token = ""
        self.audits = []
        self.currentAudit = ""
        self.isOffline = True
        
    #- Metodo de salida por defecto y de error
    @staticmethod
    def default(mensaje):
        sys.stdout.write(str(mensaje) + '\n')
    @staticmethod
    def error(mensaje):
        sys.stderr.write(str(mensaje) + '\n')

    # open a sqlite db or create if not existing
    # TODO treat possible exception for not present directory, etc. other exceptions in db methods
    def openDB(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("/var/granadav2/login.db")
        if not db.open():
            print("error")
        else:
            print("ok")
        return db
    
    def initializeDB(self):
        db = self.openDB()
        query = QSqlQuery(db)
        result = query.prepare("create if not exists table user (id integer PRIMARY KEY, email text not null, password text not null, token text)")
        if result:
            result = query.exec_()
        db.close()
        
    def loadLoginDB(self):
        db = self.openDB()
        query = QSqlQuery("select email, password, token from user", db)
        query.next()
        self.name = query.value(0)
        self.password = query.value(1)
        self.token = query.value(2)
        db.close()
    
    def saveLoginDB(self):
        db = self.openDB()
        query = QSqlQuery(db)
        query.prepare("insert into user (email, password, token) values (:email, :password, :token)")
        query.bindValue(":email", self.username)
        query.bindValue(":password", self.password)
        query.bindValue(":token", self.token)
        #bool query status
        statusCode = query.exec_()
        db.close()
        
    def deleteLogin(self):
        db = self.openDB()
        query = QSqlQuery(db)
        query.prepare("delete from user where email = :email")
        query.bindValue(":email", self.username)
        query.exec_()
        db.close()
        
    # login. if no network, use offline session
    def login(self):
        try:
            r2 = requests.post(self.APIURL + '/auth/login', data = {'email':self.email,'password':self.password})
            data = json.loads(r2.text)
            self.token = data['result']
        except Exception as e:
            #treat as offline session
            self.isOffline = True
    
    # logout. delete token, data and local file containing session data
    def logout(self):
        self.deleteLogin()
        self.username = ""
        self.password = ""
        self.token = ""
        self.audits = []
        self.currentAudit = ""
        self.isOffline = True
        #TODO remove local file
            
    def selectAudit(self, audit):
        if self.isOffline:
            # create local audit
            self.currentAudit = "local"
            self.audits.append(self.currentAudit)
            # TODO create sqlite 
        else:
            self.audit = audit
    
    def getAudits(self):
        if not self.isOffline:
            self.audits = []
            r2 = requests.post(self.APIURL + '/auth/login', data = {'email':self.username,'password':self.password})
            data = json.loads(r2.text)
            token = data['result']
            headers = {self.HeaderName:token}
            r2 = requests.get(self.APIURL + "/audit/list", headers=headers)
            jsonAudits = json.loads(r2.text)
            for audit in jsonAudits['result']:
                self.audits += str(audit['id'])
