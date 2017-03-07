#!/usr/bin/python3
#-*-coding:utf-8-*-
#- sessions class

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStatusBar, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox

class LoginDialog(QDialog):
    
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        label = QLabel("Login")
        lineEdit = QLineEdit()
        label.setBuddy(lineEdit)

        findButton = QPushButton("&Find")
        findButton.setDefault(True)

        moreButton = QPushButton("&More")
        moreButton.setCheckable(True)
        moreButton.setAutoDefault(False)

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(findButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(moreButton, QDialogButtonBox.ActionRole)

        moreButton.toggled.connect(extension.setVisible)

        topLeftLayout = QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(lineEdit)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)
        leftLayout.addWidget(caseCheckBox)
        leftLayout.addWidget(fromStartCheckBox)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.addWidget(extension, 1, 0, 1, 2)
        mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Extension")
        extension.hide()
        
        
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
