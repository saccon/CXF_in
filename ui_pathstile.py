# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pathstile.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Pathstile(object):
    def setupUi(self, Pathstile):
        Pathstile.setObjectName("Pathstile")
        Pathstile.setWindowModality(QtCore.Qt.ApplicationModal)
        Pathstile.resize(691, 169)
        self.dir = QtWidgets.QTextEdit(Pathstile)
        self.dir.setGeometry(QtCore.QRect(10, 90, 621, 31))
        self.dir.setObjectName("dir")
        self.cercadir = QtWidgets.QPushButton(Pathstile)
        self.cercadir.setGeometry(QtCore.QRect(640, 90, 31, 31))
        self.cercadir.setObjectName("cercadir")
        self.desc = QtWidgets.QTextEdit(Pathstile)
        self.desc.setGeometry(QtCore.QRect(10, 30, 621, 31))
        self.desc.setObjectName("desc")
        self.label = QtWidgets.QLabel(Pathstile)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Pathstile)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 161, 16))
        self.label_2.setObjectName("label_2")
        self.esci = QtWidgets.QPushButton(Pathstile)
        self.esci.setGeometry(QtCore.QRect(420, 130, 101, 31))
        self.esci.setObjectName("esci")
        self.esci_2 = QtWidgets.QPushButton(Pathstile)
        self.esci_2.setGeometry(QtCore.QRect(530, 130, 101, 31))
        self.esci_2.setObjectName("esci_2")

        self.retranslateUi(Pathstile)
        QtCore.QMetaObject.connectSlotsByName(Pathstile)

    def retranslateUi(self, Pathstile):
        _translate = QtCore.QCoreApplication.translate
        Pathstile.setWindowTitle(_translate("Pathstile", "Selezione path ricerca Stile grafico"))
        self.cercadir.setText(_translate("Pathstile", "..."))
        self.label.setText(_translate("Pathstile", "Descrizione dello stile"))
        self.label_2.setText(_translate("Pathstile", "Path di ricerca file QML"))
        self.esci.setText(_translate("Pathstile", "Esci e Salva "))
        self.esci_2.setText(_translate("Pathstile", "Esci senza salvare"))

