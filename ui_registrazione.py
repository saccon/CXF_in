# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_registrazione.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_regristrazione(object):
    def setupUi(self, regristrazione):
        regristrazione.setObjectName("regristrazione")
        regristrazione.resize(340, 643)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/Cxf_in/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        regristrazione.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(regristrazione)
        self.verticalLayout.setObjectName("verticalLayout")
        self.webView = QtWebKitWidgets.QWebView(regristrazione)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.esci = QtWidgets.QPushButton(regristrazione)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.esci.sizePolicy().hasHeightForWidth())
        self.esci.setSizePolicy(sizePolicy)
        self.esci.setMinimumSize(QtCore.QSize(80, 30))
        self.esci.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.esci.setObjectName("esci")
        self.verticalLayout.addWidget(self.esci)

        self.retranslateUi(regristrazione)
        QtCore.QMetaObject.connectSlotsByName(regristrazione)

    def retranslateUi(self, regristrazione):
        _translate = QtCore.QCoreApplication.translate
        regristrazione.setWindowTitle(_translate("regristrazione", "Registrazione Utente"))
        self.esci.setText(_translate("regristrazione", "Uscita"))

from PyQt5 import QtWebKitWidgets
from . import resources_rc
