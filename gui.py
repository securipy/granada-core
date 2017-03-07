#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO insert names, disclaimer
# GPL

from PyQt5.QtCore import Qt, QObject, QThread, QThreadPool, QMetaObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QWindow, QIcon, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QMenuBar, QStatusBar, QTreeWidget, QTreeWidgetItem, QTabWidget, QLineEdit, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMessageBox, QDialogButtonBox, QInputDialog
import sys, os, subprocess
from model.sessions import Session
from model.utils import system

class Granada_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        self.session = Session()
        self.moduleName = []
        self.moduleMethod =[]
        #add worker and threadpool here?
        #self.threadPool = QThreadPool()
        #self.worker =
        
        
        #GUI main objects
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.menuWidget = QTreeWidget(self.centralWidget)
        self.menuWidget.setObjectName("menuWidget")
        self.menuWidget.setHeaderLabel("Modules")
        self.menuWidget.hide()
        
        self.tabWidget= QTabWidget(self.centralWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.horizontalLayout.addWidget(self.menuWidget)
        self.horizontalLayout.addWidget(self.tabWidget)
        
        self.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        
        #create menu
        view = self.menubar.addMenu("View")
        showModules = QAction("Modules",self)
        showModules.setCheckable(True)
        showModules.setShortcut("Ctrl+M")
        showModules.triggered.connect(self.hideModules)
        view.addAction(showModules)
        
        self.loginMenu = QAction("Login", self)
        self.loginMenu.triggered.connect(self.login)
        self.logoutMenu = QAction("Logout", self)
        self.logoutMenu.triggered.connect(self.logout)
        quit = QAction("Exit",self)
        quit.setShortcut("Ctrl+Q")
        quit.triggered.connect(self.close)
        session = self.menubar.addMenu("Session")
        session.addAction(self.loginMenu)
        session.addAction(self.logoutMenu)
        session.addAction(quit)
        
        self.selectAuditAction = QAction("Select audit", self)
        self.selectAuditAction.triggered.connect(self.selectAudit)
        #self.createAuditMenu = QAction("Create audit", self)
        #self.createAuditMenu.triggered.connect(self.createAudit)
        self.auditMenu = self.menubar.addMenu("Audit")
        self.auditMenu.addAction(self.selectAuditAction)
        #audit.addAction(self.createAuditMenu)
        
        self.fillMenu()
        QMetaObject.connectSlotsByName(self)
        self.autoLogin()
        
        self.showFullScreen()
    
    def fillMenuBar(self):
        login = QAction("Login")
        login.setObjectName("Login")
        login.triggered.connect(self.login)
        logout = QAction("Logout")
        logout.setObjectName("Logout")
        logout.triggered.connect(self.logout)
        #session = self.menubar.addMenu("Session")
        session.addAction(login)
        session.addAction(logout)
        
        showModules = QAction("Modules")
        showModules.setObjectName("Modules")
        showModules.setCheckable(True)
        showModules.setShortcut("Ctrl+M")
        showModules.triggered.connect(self.hideModules)
        view = self.menubar.addMenu("View")
        view.addAction(showModules)
        
        quit = QAction("Exit")
        quit.setShortcut("Ctrl+Q")
        quit.triggered.connect(self.close)
        session = self.menubar.addMenu("Session")
        session.addAction(quit)
    
    # autoload login data from db
    def autoLogin(self):
        self.session.loadLoginDB()
        if self.session.token:
            self.loginMenu.setEnabled(False)
        else:
            self.selectAuditAction.setEnabled(False)
            self.logoutMenu.setEnabled(False)
        
        
    # ask for login credentials
    def login(self):
        loginDialog = QDialog()
        verticalLayout = QVBoxLayout()
        loginDialog.setLayout(verticalLayout)
        usernameLabel = QLabel("email")
        usernameInput = QLineEdit()
        passLabel = QLabel("password")
        passInput = QLineEdit()
        keyboardButton = QPushButton(self)
        keyboardButton.setText("Show keyboard")
        keyboardButton.clicked.connect(self.showKeyboard)
        #  TODO put checkbox to change echo mode between pass and visible
        passInput.setEchoMode(QLineEdit.Password)
        # autocomplete if login failed for sth
        if self.session.username:
            usernameInput.setText(self.session.username)
        if self.session.password:
            passInput.setText(self.session.password)
        verticalLayout.addWidget(usernameLabel)
        verticalLayout.addWidget(usernameInput)
        verticalLayout.addWidget(passLabel)
        verticalLayout.addWidget(passInput)
        verticalLayout.addWidget(keyboardButton)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        verticalLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(loginDialog.accept) 
        buttonBox.rejected.connect(loginDialog.reject) 
        result = loginDialog.exec()
        if result:
            self.session.username = usernameInput.text()
            self.session.password = passInput.text()
            loginResult = self.session.login()
            if loginResult:
                dialog = QMessageBox()
                dialog.setText("Login Successful")
                dialog.setStandardButtons(QMessageBox.Yes)
                dialog.exec()
                self.loginMenu.setEnabled(False)
                self.logoutMenu.setEnabled(True)
                self.selectAuditAction.setEnabled(True)
                
            else:
                dialog = QMessageBox()
                dialog.setText("Login failed "+ self.session.error)
                dialog.setStandardButtons(QMessageBox.Yes)
                dialog.exec()
                
    def execLogin(self):
        pass
        
    def logout(self):
        self.session.logout()
        self.loginMenu.setEnabled(True)
        self.logoutMenu.setEnabled(False)
   
    def selectAudit(self):
        self.session.getAudits()
        audits = []
        for audit in self.session.audits:
            audits.append(audit["name"])
        auditSelected = QInputDialog.getItem(self, "Audit", "Select an audit", audits, 0, False)
        if auditSelected[1]:
            for audit in self.session.audits:
                if audit["name"] == auditSelected[0]:
                    self.session.currentAudit = audit["id"]
        
    def showKeyboard(self):
        try:
            #os.system("matchbox-keyboard")
            keyboard = subprocess.Popen("xvkbd")
        except Exception as e:
            print(e)
   
    def hideModules(self):
        if not self.menuWidget.isHidden():
            self.menuWidget.hide()
        else:
            self.menuWidget.show()
    
    def fillMenu(self):
        #add layout to widget, check why reference seems to be lost
        moduleList = system.explore("modules", "modules")
        #print(module_list)
        for module in moduleList:
            aux = QTreeWidgetItem()
            aux.setData(0,0,moduleList[module])
            #get module method list
            methodList = system.explore('modules/' + moduleList[module])
            self.menuWidget.addTopLevelItem(aux)
            
            #populate module method list
            self.getMethods(moduleList[module], aux)
        
        self.menuWidget.itemDoubleClicked.connect(self.createTab)
  
    #get module methods and insert it into parent QTreeWidgetItem 
    def getMethods(self, module, parent):
        methodList = system.explore('modules/' + module)
        for counter in methodList:
            aux = QTreeWidgetItem()
            aux.setData(0,0,methodList[counter])
            parent.addChild(aux)
            
        
    def createTab(self, item, column):
        # check for root tree nodes
        if item.parent() != None:
            moduleName = item.parent().data(0,0)
            methodName = item.data(0,column)
            guiMethodName = "GUI_" + methodName
            #load module and exec (getattr)() method from class
            sys.path.append("modules/" + moduleName + "/")
            module = __import__(guiMethodName)
            newTab = getattr(module, guiMethodName)()
            # push session to modules that need it
            if hasattr(newTab, 'session'):
                print("pushing session")
                newTab.session = self.session
            newTab.setObjectName(methodName)
            self.tabWidget.addTab(newTab, newTab.objectName())
        
    def closeTab(self,index):
        close = self.createDialog("Do you want to close this tab?")
        if close:
            self.sender().removeTab(index)
       
    def createDialog(self,msg):
            dialog = QMessageBox()
            dialog.setText(msg)
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            return dialog.exec() == QMessageBox.Yes
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = Granada_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())
