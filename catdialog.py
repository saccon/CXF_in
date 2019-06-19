# -*- coding: utf-8 -*-
"""
/***************************************************************************
CARICA CXF 
                                 A QGIS plugin

                             -------------------
        begin                : 2012-09-13
        copyright            : (C) 2012 by Arch. Fabio SAccon
        email                : saccon@gisplan.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import importlib

from qgis.core import *
from qgis.utils import iface
from PyQt5.QtWidgets import *
from .ui_cercacat import Ui_cercacat
from .ui_pathstile import Ui_Pathstile
from .ui_registrazione import Ui_regristrazione
from  .memory_layer import *
from  .db_reset import *
from  .db_layer import *
from  .db_view import *
from  .db_create import *

# create the dialog for zoom to point
import urllib
import fileinput
import sys, os, imp, re
import psycopg2
import webbrowser
rpointstart = QgsRubberBand(iface.mapCanvas(),QgsWkbTypes.PointGeometry )
rpointend = QgsRubberBand(iface.mapCanvas(),QgsWkbTypes.PointGeometry )
rl=QgsRubberBand(iface.mapCanvas(),QgsWkbTypes.LineGeometry )
premuto= False
linea=False
point0=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)
point1=iface.mapCanvas().getCoordinateTransform().toMapCoordinates(0, 0)

from . import  globals

path = ""


class PointTool(QgsMapTool):
    def __init__(self, ui0,canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.ui0=ui0

    def canvasPressEvent(self, event):
        global rpointstart, rpointend, premuto, point0, point1
        if event.button() == Qt.RightButton:
            rl.reset(QgsWkbTypes.LineGeometry)
            rpointstart.reset(QgsWkbTypes.PointGeometry)
            rpointend.reset(QgsWkbTypes.PointGeometry)
            #print (point0.x(),point0.y())
            #print (point1.x(), point1.y())
            premuto = False
            self.ui0.ui.traslx.setText(str(float(self.ui0.ui.traslx.text())+ (point1.x() - point0.x())))
            self.ui0.ui.trasly.setText(str(float(self.ui0.ui.trasly.text())+(point1.y() - point0.y())))
            self.canvas.unsetMapTool(self)


            return None


        snapper = self.canvas.snappingUtils()
        result= snapper.snapToMap(event.pos())

        if not premuto:
            premuto = True
        else:
            premuto = False

        if result.isValid():
            # QMessageBox.information(None, "snap0 :"+str(premuto),str(point0.x())+" "+str(point0.y()))
            if premuto:
                point0 =  result.point()
                rpointstart.setColor(Qt.red)
                rpointstart.addPoint(point0)
            else:
                point1 =  result.point()
                rpointend.setColor(Qt.red)
                rpointend.addPoint(point1)
        else:

            if premuto:
                point0 = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos())
                rpointstart.setColor(Qt.blue)
                rpointstart.addPoint(point0)
            else:
                point1 = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos())
                rpointend.setColor(Qt.blue)
                rpointend.addPoint(point1)

                # MessageBox.information(None, "snap1 :"+str(premuto),str(point0.x())+" "+str(point0.y()))

    def canvasMoveEvent(self, event):


        global premuto, point0, point1, linea, rl
        if premuto:
            if not linea:
                rl.setColor(Qt.red)
                point2 = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos())
                rl.addPoint(point0)
                rl.addPoint(point2)
                linea = True
            else:
                if linea:
                    point2 = self.canvas.getCoordinateTransform().toMapCoordinates(event.pos())
                    rl.reset(QgsWkbTypes.LineGeometry)
                    rl.addPoint(point0)
                    rl.addPoint(point2)

    def canvasReleaseEvent(self, event):
        pass

    def activate(self):
        pass

    def deactivate(self):
        self.deactivated.emit()

    def isZoomTool(self):
        pass
class Registazione(QDialog, Ui_regristrazione):
    def __init__(self, page):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self.Page = page
        self.esci.clicked.connect(self.closediag)
        if page == "register":
            self.webView.setUrl(QUrl('https://www.prgcloud.com/auth/register.php'))
        if page == "reset":
            self.webView.setUrl(QUrl('https://www.prgcloud.com/auth/reset-pwd-req.php'))
        self.webView.show()

    def closediag(self):

        self.close()


class Pathstile(QDialog, Ui_Pathstile):
    def __init__(self, tipo):
        QDialog.__init__(self, None)
        self.Tipo = tipo
        self.setupUi(self)
        if tipo != "n":
            self.desc.setReadOnly(True)
            self.dir.setText(self.Tipo.split(":", 1)[1])
            self.desc.setText(self.Tipo.split(":", 1)[0])
        self.esci_2.clicked.connect(self.closediag)
        self.esci.clicked.connect(self.createeditstilepath)
        self.cercadir.clicked.connect(self.searchpath)

    def searchpath(self):
        # self.hide()
        read_path = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        (dirname) = QFileDialog.getExistingDirectory(self,
                                                     "Seleziona una Directory", read_path)
        self.dir.setText(dirname)

        # self.show ()

    def createeditstilepath(self):
        if self.Tipo == "n":
            if self.dir.toPlainText() != "" and self.desc.toPlainText() != "":
                with open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty', 'a') as in_file:
                    in_file.writelines(self.desc.toPlainText() + ":" + self.dir.toPlainText() + "\n")
                in_file.close()
                self.close()
            else:

                QMessageBox.information(None, "Attenzione :",
                                        "Per savare una nuova configurazione di stili /ndeve essere indicata una Descrizione e un Percorso di ricerca")
        else:

            for line in fileinput.input(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty', inplace=True):
                if line.split(":", 1)[0] == self.desc.toPlainText():
                    line = self.desc.toPlainText() + ":" + self.dir.toPlainText()
                print  (line.strip())
            fileinput.close()
        self.close()

    def closediag(self):

        self.close()


class catDialog(QDockWidget):
    def __init__(self, iface):
        QDockWidget.__init__(self, None)
        # ocon = sqlite3.connect(globals.dbName)

        self.ui = Ui_cercacat()
        self.ui.setupUi(self)
        self.ui.dbreset.clicked.connect(self.dbreset)
        self.ui.viewall.clicked.connect(self.viewall)
        self.ui.viewsel.clicked.connect(self.viewsel)
        self.ui.cxfspatialite.clicked.connect(self.dbloadcxf)
        self.ui.workdir.clicked.connect(self.setdircxf)
        self.ui.listfogli.itemClicked.connect(self.testapath)
        self.ui.getpoint.clicked.connect(self.getpoint)
        self.ui.applytrasf.clicked.connect(self.applytrasf)
        self.ui.applytrasfall.clicked.connect(self.applytrasfall)
        self.ui.geoconn.clicked.connect(self.connectgeodb)
        self.ui.registrazione.clicked.connect(self.userreg)
        self.ui.rstpwd.clicked.connect(self.resetpwd)
        self.ui.cxfmemory.clicked.connect(self.cxfmemory)
        self.ui.dbdeletefg.clicked.connect(self.deletefg)
        self.ui.dbdeletecom.clicked.connect(self.deletecom)
        self.ui.toolBox.currentChanged.connect(self.ric_mapp)
        self.ui.cat_com.currentIndexChanged.connect(self.populatericercaFogli)
        self.ui.del_cat_com.currentIndexChanged.connect(self.populatedeleteFogli)
        self.ui.cat_fg.currentIndexChanged.connect(self.populateMapp)
        self.ui.gisplan.clicked.connect(self.info)
        self.ui.donate.clicked.connect(self.donate)
        self.ui.listcomune.itemClicked.connect(self.Fogli_selezione)
        self.ui.selstile.clicked.connect(self.stile_selezione)
        self.ui.editstile.clicked.connect(self.edit_style)
        self.ui.newstile.clicked.connect(self.create_style)
        self.ui.delstile.clicked.connect(self.del_style)
        self.ui.paramdb.clicked.connect(self.paramdb)
        self.ui.test.clicked.connect(self.test)
        self.ui.postgis.clicked.connect(self.postgis)
        self.ui.changetrasf.hide()
        self.ui.georef_db.hide()
        self.ui.etrs89_db.hide()
        self.ui.Regionefvg.hide()
        self.db_init()


        db_create(self)

        self.populateVisualizzaione()

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Cxf_in", self.action)
        self.iface.removeToolBarIcon(self.action)

    def del_style(self):
        item = self.ui.lststile.invisibleRootItem()
        for i in range(item.childCount()):
            if item.child(i).isSelected():
                for line in fileinput.input(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty',
                                            inplace=True):
                    if line.split(":", 1)[0] == item.child(i).text(0):
                        continue
                    else:
                      print  (line,)

        self.populatestili()

    def edit_style(self):
        item = self.ui.lststile.invisibleRootItem()
        for i in range(item.childCount()):
            if item.child(i).isSelected():
                self.dlg = Pathstile(item.child(i).text(0) + ":" + item.child(i).data(0, Qt.UserRole))
                self.dlg.show()
                result = self.dlg.exec_()
                self.populatestili()

    def create_style(self):
        self.dlg = Pathstile("n")
        self.dlg.show()
        result = self.dlg.exec_()
        self.populatestili()

    def info(self):
        webbrowser.open("http://www.gisplan.it")

    def donate(self):
        webbrowser.open("https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=28M43B8FURPNW")

    def userreg(self):
        self.dlg = Registazione("register")
        self.dlg.show()
        result = self.dlg.exec_()

    def resetpwd(self):
        self.dlg = Registazione("reset")
        self.dlg.show()
        result = self.dlg.exec_()

    def connectgeodb(self):
        if self.ui.geoconn.text() == "Disconnetti Utente":
            self.ui.georef_db.hide()
            self.ui.etrs89_db.hide()
            self.ui.Regionefvg.hide()
            self.ui.label_13.setText("Registrazione utente per georeferenziazione")
            self.ui.label_14.show()
            self.ui.label_15.show()
            self.ui.label_16.show()
            self.ui.user.show()
            self.ui.password.show()
            self.ui.rstpwd.show()
            self.ui.registrazione.show()

            self.ui.user.setReadOnly(False)
            self.ui.password.setReadOnly(False)
            self.ui.user.setAutoFillBackground(False)
            self.ui.user.setStyleSheet("QLineEdit{ background-color :  rgb(255, 255, 255); color :  rgb(0, 0, 0); }")
            self.ui.user.setText("")
            self.ui.password.setAutoFillBackground(False)
            self.ui.password.setText("")
            self.ui.password.setStyleSheet(
                "QLineEdit{ background-color :  rgb(255, 255, 255); color :  rgb(0, 0, 0); }")
            self.ui.geoconn.setText("Connessione al server di georeferenziazione")

        else:
            try:

                req = 'http://www.prgcloud.com/auth/usercheck.php?username=' + self.ui.user.text() + '&password=' + self.ui.password.text()
                try:

                    with contextlib.closing(urllib.request.urlopen(req)) as x:
                        for line in x:
                            #print (line)
                            html = line
                            break
                except urllib.URLError as err:
                    print (err)

                user = html.decode("utf-8").split("|")
                if user[0].replace('<br />','').strip() == 'verificato':
                    print(user[2].replace('<br />','').strip())
                    if user[2].replace('<br />','').strip()== '1':
                        print(user[1].strip())
                        self.ui.changetrasf.show()
                    self.ui.georef_db.show()
                    self.ui.etrs89_db.show()
                    self.ui.Regionefvg.show()
                    self.ui.label_13.setText("Bentornato " + user[1])
                    self.ui.label_14.hide()
                    self.ui.label_15.hide()
                    self.ui.label_16.hide()
                    self.ui.user.hide()
                    self.ui.password.hide()
                    self.ui.rstpwd.hide()
                    self.ui.registrazione.hide()

                    self.ui.user.setReadOnly(True)
                    self.ui.password.setReadOnly(True)
                    self.ui.user.setAutoFillBackground(True)
                    self.ui.user.setStyleSheet(
                        "QLineEdit{ background-color :  rgb(244, 217, 221); color :  rgb(0, 0, 255); }")
                    self.ui.password.setAutoFillBackground(True)

                    self.ui.password.setStyleSheet(
                        "QLineEdit{ background-color :  rgb(244, 217, 221); color :  rgb(0, 0, 255); }")
                    self.ui.geoconn.setText("Disconnetti Utente")

                    msgBox = QMessageBox()
                    msgBox.setText('Utente riconosciuto')
                    msgBox.addButton(QPushButton('OK'), QMessageBox.YesRole)

                    bottone = QPushButton("Supporta lo Sviluppo")
                    bottone.setIcon(QIcon(':/plugins/Cxf_in/paypal.png'))
                    bottone.setIconSize(QSize(80, 25))
                    msgBox.addButton(bottone, QMessageBox.NoRole)
                    # msgBox.setIconPixmap(QPixmap(':/plugins/Cxf_in/paypal.png'))
                    ex = msgBox.exec_()
                    if ex == 1:
                        # QMessageBox.information(None, "Avviso :","Utente riconosciuto"+str(ex))
                        webbrowser.open(
                            "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=28M43B8FURPNW")


                else:
                    if html != "":
                        QMessageBox.information(None, "Errore :", "Utente o password errati")


                    else:
                        QMessageBox.information(None, "Errore :", "Devono essere inseriti user e password")

            except ValueError:
                QMessageBox.information(None, "Errore :", "il database non è stato connesso/n verifica le credenziali.")
                # print "ERROR IN CONNECTION"

    def viewall(self):
        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()
        ocur.execute("delete  FROM " + globals.schema + "selezione")
        globals.ocon.commit()
        ocur.execute(
            "INSERT INTO " + globals.schema + "selezione  (Nomefile,Codice_comune,Sez,Fg,Sel)  select distinct Nomefile,Codice_comune,Sez,Fg, '1' from " + globals.schema + "particelle order by Nomefile")
        globals.ocon.commit()
        self.populateVisualizzaione()

        if self.ui.singolfg.isChecked():
            lista = "((EXT='') or (Ext is Null))"
        else:
            lista = " "

        db_view_all(self, lista)

        iface.mapCanvas().zoomToFullExtent()

    def viewsel(self):
        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()
        ocur.execute("select distinct Nomefile,Sel from " + globals.schema + "selezione order by Nomefile")

        lista = "("
        for d in ocur:
            if d[1] == "1":
                lista += "'" + d[0] + "',"
        lista = lista[:-1] + ")"

        if lista != ")":

            lista = "Nomefile IN " + lista
            if self.ui.singolfg.isChecked():
                lista = lista + " AND ((EXT='') or (Ext is Null))"

                db_view_sel(self, lista)

        else:
            lista = "Nomefile=='9999'"

        db_view_sel(self, lista)

        iface.mapCanvas().zoomToFullExtent()

    def dbreset(self):
        db_delete(self)
        db_create(self)

    def deletefg(self):
        uri = QgsDataSourceUri()
        uri.setDatabase(globals.dbName)
        uri.setDataSource('', 'Particelle', 'geom')
        vl_part = QgsVectorLayer(uri.uri(), 'Particelle', 'spatialite')
        uri.setDataSource('', 'Fabbricati', 'geom')
        vl_ed = QgsVectorLayer(uri.uri(), 'Fabbricati', 'spatialite')
        uri.setDataSource('', 'Strade', 'geom')
        vl_st = QgsVectorLayer(uri.uri(), 'Strade', 'spatialite')
        uri.setDataSource('', 'Confine', 'geom')
        vl_conf = QgsVectorLayer(uri.uri(), 'Confine', 'spatialite')
        uri.setDataSource('', 'Acque', 'geom')
        vl_aq = QgsVectorLayer(uri.uri(), 'Acque', 'spatialite')
        uri.setDataSource('', 'Linee', 'geom')
        vl_linee = QgsVectorLayer(uri.uri(), 'Linee', 'spatialite')
        uri.setDataSource('', 'Simboli', 'geom')
        vl_point = QgsVectorLayer(uri.uri(), 'Simboli', 'spatialite')
        uri.setDataSource('', 'Testi', 'geom')
        vl_testo = QgsVectorLayer(uri.uri(), 'Testi', 'spatialite')
        uri.setDataSource('', 'Fiduciali', 'geom')
        vl_fidu = QgsVectorLayer(uri.uri(), 'Fiduciali', 'spatialite')
        #layers = QgsProject.instance().mapLayers()
        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()

        codcom = ""
        codsez = ""

        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        # print (self.ui.del_cat_com.currentText())
        if (self.ui.del_cat_com.currentText()) != comune:
            for ctcom in testo:
                line = ctcom.split(",")

                if line[3].strip() == self.ui.del_cat_com.currentText():
                    # print line[0].strip()
                    codcom = line[0].strip()
                    if line[1].strip() == '':
                        codsez = "_"
                    else:
                        codsez = line[1].strip()
        nfile = codcom + codsez + self.ui.del_cat_fg.currentText().replace("_", "")
        print(nfile)
        ret = QMessageBox.question(None, "ATTENZIONE",
                                   "Vuoi veramente cancellare il foglio " + nfile + " del Comune " + self.ui.del_cat_com.currentText(),
                                   QMessageBox.Yes, QMessageBox.No)

        if ret == QMessageBox.Yes:
            ocur.execute("delete from " + globals.schema + "particelle where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "fabbricati where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Strade where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Confine where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Acque where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Linee where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Simboli where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Testi where nomefile='" + nfile + "'")
            ocur.execute("delete from " + globals.schema + "Fiduciali where nomefile='" + nfile + "'")
            vl_ed.updateExtents()
            vl_st.updateExtents()
            vl_aq.updateExtents()
            vl_conf.updateExtents()
            vl_linee.updateExtents()
            vl_point.updateExtents()
            vl_testo.updateExtents()
           #ocur.execute('VACUUM')
            globals.ocon.commit()
        ocur.close()

    def deletecom(self):
        uri = QgsDataSourceUri()
        if self.testdb() and self.ui.postgis.isChecked():

            uri.setConnection(str(globals.line[0]), "5432", str(globals.line[1]), str(globals.line[2]),
                              str(globals.line[3]))
        else:
            uri.setDatabase(globals.dbName)

        uri.setDataSource(globals.schema.replace(".", ""), 'particelle', 'geom')
        vl_part = QgsVectorLayer(uri.uri(), 'Particelle', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'fabbricati', 'geom')
        vl_ed = QgsVectorLayer(uri.uri(), 'Fabbricati', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'strade', 'geom')
        vl_st = QgsVectorLayer(uri.uri(), 'Strade', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'confine', 'geom')
        vl_conf = QgsVectorLayer(uri.uri(), 'Confine', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'acque', 'geom')
        vl_aq = QgsVectorLayer(uri.uri(), 'Acque', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'linee', 'geom')
        vl_linee = QgsVectorLayer(uri.uri(), 'Linee', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'simboli', 'geom')
        vl_point = QgsVectorLayer(uri.uri(), 'Simboli', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'testi', 'geom')
        vl_testo = QgsVectorLayer(uri.uri(), 'Testi', globals.datadb)
        uri.setDataSource(globals.schema.replace(".", ""), 'fiduciali', 'geom')
        vl_fidu = QgsVectorLayer(uri.uri(), 'Fiduciali', globals.datadb)
        globals.ocon.commit()
        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()

        codcom = ""
        codsez = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        # print (self.ui.del_cat_com.currentText())
        if (self.ui.del_cat_com.currentText()) != comune:
            for ctcom in testo:
                line = ctcom.split(",")

                if line[3].strip() == self.ui.del_cat_com.currentText():
                    # print line[0].strip()
                    codcom = line[0].strip()
                    if line[1].strip() == '':
                        codsez = "_"
                    else:
                        codsez = line[1].strip()

        ret = QMessageBox.question(None, "ATTENZIONE",
                                   "Vuoi veramente cancellare il Comune " + self.ui.del_cat_com.currentText(),
                                   QMessageBox.Yes, QMessageBox.No)

        if ret == QMessageBox.Yes:
            ocur.execute(
                "delete from " + globals.schema + "particelle where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "fabbricati where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Strade where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Confine where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Acque where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Linee where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Simboli where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Testi where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            ocur.execute(
                "delete from " + globals.schema + "Fiduciali where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")
            vl_ed.updateExtents()
            vl_part.updateExtents()
            vl_st.updateExtents()
            vl_aq.updateExtents()
            vl_conf.updateExtents()
            vl_linee.updateExtents()
            vl_point.updateExtents()
            vl_testo.updateExtents()
            vl_fidu.updateExtents()

            # ocur.execute("vacuum")
            globals.ocon.commit()
        ocur.close()
        self.populatedelete()

    def paramdb(self):
        if self.testdb():
            self.savedb()
            QMessageBox.information(None, "Connessione POSTGIS :", "Parametri salvati in memoria")
        else:
            QMessageBox.information(None, "Attenzione :", "I parametri non sono stati salvati")

    def savedb(self):
        if self.testdb():
            out_file = open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/')  + '/db_conf.ini', "w")
            out_file.writelines(self.ui.server.text() + "\n")
            out_file.writelines(self.ui.database.text() + "\n")
            out_file.writelines(self.ui.user_2.text() + "\n")
            out_file.writelines(self.ui.passwd.text() + "\n")
            out_file.writelines(str(self.ui.postgis.checkState()) + "\n")
            out_file.close()
        else:
            out_file = open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/')  + '/db_conf.ini', "w")
            out_file.writelines("\n")
            out_file.writelines("\n")
            out_file.writelines("\n")
            out_file.writelines("\n")
            out_file.writelines("\n")
            out_file.close()
        import importlib
        importlib.reload (globals)
        print("savedb")
        db_create(self)

        self.populatedelete()

    def db_init(self):
        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/account.ini'):
            with open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/account.ini', "r") as lines:
                line = lines.read().splitlines()
                self.ui.user.setText(line[0])
                self.ui.password.setText(line[1])

        if os.path.isfile(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/db_conf.ini'):
            with open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/db_conf.ini', "r") as lines:
                line = lines.read().splitlines()
                self.ui.server.setText(line[0])
                self.ui.database.setText(line[1])
                self.ui.user_2.setText(line[2])
                self.ui.passwd.setText(line[3])

                if line[4] == "2":

                    self.ui.postgis.setChecked(True)
                    self.ui.toolBox.setItemText(0, "Visualizzazione Fogli PostGis")
                    self.ui.toolBox.setItemText(3, "Carica CXF su DB PostGis")
                    self.ui.cxfspatialite.setText("Importa files CXF nel DB PostGis")
                    self.ui.dbreset.setText("Svuota intero DB PostGis")
                else:
                    self.ui.postgis.setChecked(False)
                    self.ui.toolBox.setItemText(0, "Visualizzazione Fogli SpatiaLite")
                    self.ui.toolBox.setItemText(3, "Carica CXF su DB SpatiaLite")
                    self.ui.cxfspatialite.setText("Importa files CXF nel DB SpatiaLite")
                    self.ui.dbreset.setText("Svuota intero DB SpatiaLite")
            lines.close()

    def testdb(self):
        try:
            db = psycopg2.connect(dbname=self.ui.database.text(), port=5432, user=self.ui.user_2.text(),
                                  password=self.ui.passwd.text(), host=self.ui.server.text())

            return True
        except:

            self.ui.postgis.setChecked(False)
            return False

    def test(self):

        if self.testdb():
            QMessageBox.information(None, "Attenzione :", "Connessione avvenuta a POSTGIS")
        else:
            QMessageBox.information(None, "Attenzione :", "Impossibilie connettersi a POSTGIS")

    def postgis(self):
        self.savedb()
        for parent in QgsProject.instance().layerTreeRoot().children():
            if isinstance(parent, QgsLayerTreeGroup):
                if parent.name() == "Catasto":
                    QgsProject.instance().layerTreeRoot().removeChildNode(parent)
        # indice = iface.legendInterface().groups()
        # if 'Catasto' in indice:
        #     iface.legendInterface().removeGroup(indice.index('Catasto'))

        if self.testdb() and self.ui.postgis.isChecked():

            QMessageBox.information(None, "PostGis:", "Pronto a lavorare con PostGis")
            self.ui.toolBox.setItemText(0, "Visualizzazione Fogli PostGis")
            self.ui.toolBox.setItemText(3, "Carica CXF su DB PostGis")
            self.ui.cxfspatialite.setText("Importa files CXF nel DB PostGis")
            self.ui.dbreset.setText("Svuota intero DB PostGis")
        else:

            QMessageBox.information(None, "PostGis:", "Pronto a lavorare con Spatialite")
            self.ui.toolBox.setItemText(0, "Visualizzazione Fogli SpatiaLite")
            self.ui.toolBox.setItemText(3, "Carica CXF su DB SpatiaLite")
            self.ui.cxfspatialite.setText("Importa files CXF nel DB SpatiaLite")
            self.ui.dbreset.setText("Svuota intero DB SpatiaLite")

    def dbloadcxf(self):
        db_load(self,"")


    def setdircxf(self):
        def addParent(parent, column, title, data):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setExpanded(False)

            return item

        def addChild(parent, column, title, data):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)

            return item
        if os.path.exists(os.getenv("HOME") + '/workpath'):
            fpath = open(os.getenv("HOME") + '/workpath', 'r')
            read_path = fpath.read()
            fpath.close
        else:
            read_path = "."
        (dirname) = QFileDialog.getExistingDirectory(iface.mainWindow(),
                                                          "Seleziona la directory dei cxf ...", read_path,QFileDialog.ShowDirsOnly)

        if len(dirname) == 0:
            return

        fpath = open(os.getenv("HOME") + '/workpath', 'w')
        fpath.write(os.path.dirname(dirname+"/"))
        fpath.close
        self.ui.listfogli.setRootIsDecorated(False)
        self.ui.listfogli.clear()
        self.ui.listfogli.header().setSortIndicator(0, Qt.AscendingOrder)
        self.ui.listfogli.setSelectionMode(QAbstractItemView.SingleSelection)
        for root, dirs, files in os.walk(dirname):
          for filename in files:
            if ".cxf" in filename:
                parent = addParent(self.ui.listfogli.invisibleRootItem(), 0, filename.replace(".cxf",""), dirname+"/"+filename)
                print(filename)

    def testapath(self):

        getSelected = self.ui.listfogli.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)

            print (getChildNode)

            print (baseNode.data(0, Qt.UserRole))


            req = 'https://www.prgcloud.com/auth/settransform.php?username=' + self.ui.user.text() + '&password=' + self.ui.password.text() + '&foglio=' +baseNode.text(0)


            html = ""
            print(req)
            self.ui.georef_db.setChecked(True)
            try:
                with contextlib.closing(urllib.request.urlopen(req)) as x:
                    for line in x:
                        html = line.decode()
                        break
            except urllib.URLError as err:
                QMessageBox.information(None, "Avviso :", "Errore " + str(err) + file.split(".")[0])
                return
            if html.strip() == "":
                QMessageBox.information(None, "Avviso :", "Errore trasformazione non trovata  "+ file.split(".")[0])
                setattr(foglio, "foglio", file.split(os.extsep, 1)[0])
                setattr(foglio, "metodo", "")
                return

            while html.find("\n\n") > 0:
                html = html.replace("\n\n", "\n")
            docxml = (
            html.replace("&lt;", "<").replace("&gt;", ">").replace("<br />", "").replace("\r", "").replace("\t", ""))
            while docxml.find("\n\n") > 0:
                docxml = docxml.replace("\n\n", "\n")
            doc = etree.fromstring(docxml)
            for root in doc.findall("."):
                setattr(foglio, "foglio", baseNode.text(0))
                for imp in root.find("./trasformazioneF"):
                    if imp.tag != "Origine":
                        setattr(foglio, imp.tag, imp.text)
            doc = etree.fromstring(docxml)
            for imp in doc.findall("./trasformazioneF/Origine/"):
                if imp.tag in ("codice", "ValidoDa", "ValidoA"):
                    setattr(matrix, imp.tag, imp.text)
                else:

                    setattr(matrix, imp.tag, float(imp.text))

            self.ui.traslx.setText(foglio.traslx)
            self.ui.trasly.setText (foglio.trasly)
            self.ui.orig.setText(foglio.orig)
            self.ui.rotang.setText(foglio.rotang)
            self.ui.scalex.setText(foglio.scalex)
            self.ui.scaley.setText(foglio.scaley)


    def getpoint(self):



        passo=0
        tool = PointTool(self,iface.mapCanvas())
        iface.mapCanvas().setMapTool(tool)
        #iface.mapCanvas().deactivated.connect(self.donate())

        print (passo)
        print (point0.x(), point0.y())
        print (point1.x(), point1.y())
        passo=1
        # self.ui.traslx.setText (str(point0.x()-point1.x()))
        # self.ui.trasly.setText(str(point0.y() - point1.y()))
        #iface.mapCanvas().setMapTool(tool)

    def applytrasfall(self):
        foglio.traslx = self.ui.traslx.text()
        foglio.trasly = self.ui.trasly.text()
        foglio.orig = self.ui.orig.text()
        foglio.rotang = self.ui.rotang.text()
        foglio.scalex = self.ui.scalex.text()
        foglio.scaley = self.ui.scaley.text()
        item = self.ui.listfogli.invisibleRootItem()
        for i in range(item.childCount()):
            req = 'https://www.prgcloud.com/auth/settransform.php?username=' + self.ui.user.text() + '&password=' + self.ui.password.text() + '&foglio=' +item.child(i).text(0)\
                  + '&traslx=' + foglio.traslx + '&trasly=' + foglio.trasly + '&orig=' + foglio.orig + '&rotang=' + foglio.rotang + '&scalex=' + foglio.scalex + '&scaley=' + foglio.scaley
            try:
                with contextlib.closing(urllib.request.urlopen(req)) as x:
                    for line in x:
                        html = line.decode()
                        break
            except urllib.URLError as err:
                QMessageBox.information(None, "Avviso :", "Errore " + str(err) + file.split(".")[0])
                return
            db_load(self, item.child(i).data(0, Qt.UserRole))
        iface.mapCanvas().refreshAllLayers()


    def applytrasf(self):
        foglio.traslx=self.ui.traslx.text()
        foglio.trasly=self.ui.trasly.text()
        foglio.orig=self.ui.orig.text()
        foglio.rotang=self.ui.rotang.text()
        foglio.scalex=self.ui.scalex.text()
        foglio.scaley=self.ui.scaley.text()

        getSelected = self.ui.listfogli.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            #print (baseNode.data(0, Qt.UserRole))
            req = 'https://www.prgcloud.com/auth/settransform.php?username=' + self.ui.user.text() + '&password=' + self.ui.password.text() + '&foglio=' +baseNode.text(0)+ '&traslx='+foglio.traslx+ '&trasly='+foglio.trasly+'&orig='+foglio.orig+'&rotang='+foglio.rotang+'&scalex='+foglio.scalex+'&scaley='+foglio.scaley
            print (req)
            try:
                with contextlib.closing(urllib.request.urlopen(req)) as x:
                    for line in x:
                        html = line.decode()
                        break
            except urllib.URLError as err:
                QMessageBox.information(None, "Avviso :", "Errore " + str(err) + file.split(".")[0])
                return
        db_load(self, baseNode.data(0, Qt.UserRole))
        iface.mapCanvas().refreshAllLayers()
    def ric_mapp(self):

        if self.ui.toolBox.currentIndex() == 1:
            #layers = QgsProject.instance().mapLayers()
            okpart = False
            for parent in QgsProject.instance().layerTreeRoot().children():
                if isinstance(parent, QgsLayerTreeGroup):
                    if parent.name() == "Catasto":
                        for layer in parent.children():
                            if layer.name() == 'Particelle':
                                okpart = True

            #for name, layid in layers.iteritems():
                #if layid.name() == 'Particelle':
                   # okpart = True
            if okpart:

                self.populateRicerca()
        if self.ui.toolBox.currentIndex() == 5:
            self.populatestili()
        if self.ui.toolBox.currentIndex() == 0:
            self.populateVisualizzaione()
        if self.ui.toolBox.currentIndex() == 4:
            self.populatedelete()

    def cxfmemory(self):
        if os.path.exists(os.getenv("HOME") + '/workpath'):
            fpath = open(os.getenv("HOME") + '/workpath', 'r')
            read_path = fpath.read()
            fpath.close
        else:
            read_path = "."
        (filename, filter) = QFileDialog.getOpenFileNames(iface.mainWindow(),
                                                                   "Seleziona un file cxf da caricare...", read_path,
                                                                   "CXF files (*.cxf)",
                                                                   "Filtro per selezione file")
        if len(filename) == 0:
            return
        memory_layer(self, filename)

    def stile_selezione(self):
        item = self.ui.lststile.invisibleRootItem()
        for i in range(item.childCount()):
            if item.child(i).isSelected():
                self.ui.attstile.setText(item.child(i).text(0))
                for line in fileinput.input(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty',inplace=True):
                    if line[:4] == "att:":
                        line = "att:" + item.child(i).text(0) + ":" + item.child(i).data(0, Qt.UserRole)
                    print  (line.strip())
        db_view_change_style()

    def Fogli_selezione(self, item, column):
        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()

        if item.checkState(column) == Qt.Checked:
            if item.parent():
                # selezione  il foglio per comune selezionato
                ocur.execute("update " + globals.schema + "selezione set sel='1' where Nomefile='" + item.data(0, Qt.UserRole) + "'")
                globals.ocon.commit()
                allview = True
                for i in range(item.parent().childCount()):
                    if item.parent().child(i).checkState(column) == Qt.Unchecked:
                        allview = False
                if allview == True:
                    item.parent().setCheckState(column, Qt.Checked)
            else:
                # selezione tutti i fogli per comune selezionato
                for i in range(item.childCount()):
                    item.child(i).setCheckState(column, Qt.Checked)
                ocur.execute("update " + globals.schema + "selezione set Sel='1' where Codice_comune='" + item.data(0,
                                                                                                                    Qt.UserRole)[
                                                                                                          0:4] + "' and Sez='" + item.data(
                    0, Qt.UserRole)[4:5] + "'")
                globals.ocon.commit()

        else:
            if item.parent():
                item.parent().setCheckState(column, Qt.Unchecked)
                ocur.execute("update " + globals.schema + "selezione set Sel=Null where Nomefile='" + item.data(0,
                                                                                                                Qt.UserRole) + "'")
                globals.ocon.commit()
            else:
                # deselezione tutti i fogli per comune selezionato
                for i in range(item.childCount()):
                    item.child(i).setCheckState(column, Qt.Unchecked)
                    # print item.data(0, Qt.UserRole)
                ocur.execute("update " + globals.schema + "selezione set Sel=Null where Codice_comune='" + item.data(0,
                                                                                                                     Qt.UserRole)[
                                                                                                           0:4] + "' and Sez='" + item.data(
                    0, Qt.UserRole)[4:5] + "'")
                globals.ocon.commit()

    def populatestili(self):
        def addParent(parent, column, title, data):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setExpanded(True)

            return item

        self.ui.lststile.clear()
        in_file = open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty', 'r')
        #print (os.getenv("HOME"))
        for line in in_file:
            if line.find(":") > 0:
                if line[:4] != "att:":
                    campo = line.split(":", 1)
                    parent = addParent(self.ui.lststile.invisibleRootItem(), 0, campo[0], campo[1])
            else:
                if line.find(":")> 0 :
                    campo = line.split(":", 2)
                    self.ui.attstile.setText(campo[1])
        in_file.close()

    def populateVisualizzaione(self):
        import importlib
        importlib.reload (globals)
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        in_file.close

        def addParent(parent, column, title, data, sel):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setExpanded(False)
            item.setCheckState(column, sel)
            return item

        def addChild(parent, column, title, data, sel):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            item.setCheckState(column, sel)
            return item
            # ocon = sqlite3.connect(globals.dbName)

        ocur = globals.ocon.cursor()

        #print ('insert into ' + globals.schema + 'selezione (Codice_comune,Sez,Fg,Nomefile)  SELECT distinct Codice_comune,Fg,Nomefile  from ' + globals.schema + 'particelle  where Nomefile not in (select Nomefile from ' + globals.schema + 'selezione)')
        try:
            ocur.execute(
                'insert into ' +  globals.schema + 'selezione (Codice_comune,Sez,Fg,Nomefile)  SELECT distinct Codice_comune,Sez,Fg,Nomefile  from ' +  globals.schema + 'particelle  where Nomefile not in (select Nomefile from ' +  globals.schema + 'selezione)')

            globals.ocon.commit()
            ocur.execute(
                'delete from ' + globals.schema + 'selezione where Nomefile in (SELECT  Nomefile  from ' + globals.schema + 'selezione  where Nomefile not in (select distinct Nomefile from ' + globals.schema + 'particelle))')
            globals.ocon.commit()
            self.ui.listcomune.clear()
            ocur.execute('select Codice_comune,Fg,Nomefile,Sel,Sez from ' + globals.schema + 'selezione order by Nomefile')
            comune = ""
            sez = ""
            for d in ocur:
                if d[3] == "1":
                    selezionato = Qt.Checked
                else:
                    selezionato = Qt.Unchecked

                if ((d[0]) != comune) or ((d[4]) != sez):
                    for ctcom in testo:
                        line = ctcom.split(",")
                        if d[4] == "_":
                            if line[0].strip() == d[0]:
                                desccom = line[0]+"-"+line[1]+"-"+ line[3].strip()
                        else:
                            if line[0].strip() == d[0] and line[1].strip() == d[4]:
                                desccom = line[0]+"-"+line[1]+"-"+ line[3].strip()
                    parent = addParent(self.ui.listcomune.invisibleRootItem(), 0, desccom, d[0] + d[4], selezionato)
                    addChild(parent, 0, d[2][4:5] + "_" + d[2][5:9] + "_" + d[2][9:10] + "_" + d[2][10:11], d[2],
                             selezionato)
                    comune = d[0]
                    sez = d[4]
                else:
                    item = addChild(parent, 0, d[2][4:5] + "_" + d[2][5:9] + "_" + d[2][9:10] + "_" + d[2][10:11], d[2],
                                    selezionato)
                    if selezionato == Qt.Unchecked:
                        item.parent().setCheckState(0, Qt.Unchecked)
        except:
            pass

    def populateRicerca(self):
        print ('kkk')
        codcom = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        self.ui.cat_com.setEditable(True)
        self.ui.cat_com.clear()

        # ocon = sqlite3.connect(globals.dbName)

        ocur = globals.ocon.cursor()
        ocur.execute("SELECT distinct Codice_comune,Sez from " + globals.schema + "selezione where sel='1'")
        globals.ocon.commit()
        comune = ""
        myListA = []
        for d in ocur:
            if (d[0]) != comune:
                for ctcom in testo:
                    line = ctcom.split(",")
                    if line[1].strip() == '':
                        sezione = "_"
                    else:
                        sezione = line[1].strip()
                    if line[0].strip() == d[0] and sezione == d[1]:
                        desccom = line[3].strip()

            print (desccom)
            myListA.append(desccom)

        self.ui.cat_com.addItems(myListA)

    def populatedelete(self):
        codcom = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        self.ui.del_cat_com.setEditable(True)
        self.ui.del_cat_com.clear()

        # ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()
        ocur.execute('SELECT distinct Codice_comune,Sez from ' + globals.schema + 'particelle')
        # print 'SELECT distinct Codice_comune from ' + globals.schema + 'particelle'
        globals.ocon.commit()

        myListA = []
        for d in ocur:
            if (d[0]) != comune:
                for ctcom in testo:
                    line = ctcom.split(",")
                    if line[1].strip() == '':
                        sezione = "_"
                    else:
                        sezione = line[1].strip()
                    if line[0].strip() == d[0] and sezione == d[1]:
                        desccom = line[3].strip()

            myListA.append(desccom)

        self.ui.del_cat_com.addItems(myListA)

    def populatericercaFogli(self):
        codcom = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        if (self.ui.cat_com.currentText()) != comune:
            for ctcom in testo:
                line = ctcom.split(",")

                if line[3].strip() == self.ui.cat_com.currentText():
                    # print line[0].strip()
                    codcom = line[0].strip()
                    if line[1].strip() == '':
                        codsez = "_"
                    else:
                        codsez = line[1].strip()

        self.ui.cat_fg.setEnabled(True)
        self.ui.cat_fg.setEditable(True)

        self.ui.cat_fg.clear()

        # ocon = sqlite3.connect(globals.dbName)

        ocur = globals.ocon.cursor()

        ocur.execute(
            "SELECT distinct Nomefile from " + globals.schema + "selezione where Codice_comune='" + codcom + "' and Sez='" + codsez + "' and sel='1'")

        globals.ocon.commit()

        lista = []
        for d in ocur:
            lista.append(d[0][4:5] + "_" + d[0][5:9] + "_" + d[0][9:10] + "_" + d[0][10:11])
        self.ui.cat_fg.addItems(sorted(lista))
        self.ui.cat_fg.clearEditText()

    def populatedeleteFogli(self):
        codcom = ""
        codsez = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()

        for ctcom in testo:
            line = ctcom.split(",")

            if line[3].strip() == self.ui.del_cat_com.currentText():

                codcom = line[0].strip()
                if line[1].strip() == '':
                    codsez = "_"
                else:
                    codsez = line[1].strip()

        self.ui.del_cat_fg.setEnabled(True)
        self.ui.del_cat_fg.setEditable(True)

        self.ui.del_cat_fg.clear()

        # ocon = sqlite3.connect(globals.dbName)
        globals.ocon.commit()
        ocur = globals.ocon.cursor()
        ocur.execute(
            "SELECT distinct Nomefile from " + globals.schema + "particelle where Codice_comune='" + codcom + "' and Sez='" + codsez + "'")

        globals.ocon.commit()

        lista = []
        for d in ocur:
            lista.append(d[0][4:5] + "_" + d[0][5:9] + "_" + d[0][9:10] + "_" + d[0][10:11])
        self.ui.del_cat_fg.addItems(sorted(lista))
        self.ui.del_cat_fg.clearEditText()

    def populateMapp(self):
        codcom = ""
        codsez = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        if (self.ui.cat_com.currentText()) != comune:
            for ctcom in testo:
                line = ctcom.split(",")

                if line[3].strip() == self.ui.cat_com.currentText():
                    # print line[0].strip()
                    codcom = line[0].strip()

                    if line[1].strip() == '':
                        codsez = "_"
                    else:
                        codsez = line[1].strip()

        self.ui.cat_mapp.setEditable(True)
        self.ui.cat_mapp.clear()

        # ocon = sqlite3.connect(globals.dbName)

        ocur = globals.ocon.cursor()
        #print (codcom + codsez + self.ui.cat_fg.currentText()[2:255].replace("_", ""))

        # print "SELECT distinct Mappale||'-'||denom from " + globals.schema + "Particelle where Nomefile='"+codcom+self.ui.cat_fg.currentText().replace ("_","")+"'"
        ocur.execute(
            "SELECT distinct Mappale||coalesce('-'||denom ,'') from " + globals.schema + "Particelle where Nomefile='" + codcom + codsez + self.ui.cat_fg.currentText()[
                                                                                                                                           2:255].replace(
                "_", "") + "'")

        globals.ocon.commit()
        self.ui.cat_mapp.setEnabled(True)
        lista = []
        for d in ocur:
            lista.append(d[0])

        self.ui.cat_mapp.addItems(sorted(lista))
        self.ui.cat_mapp.clearEditText()
        self.ui.cat_mapp.currentIndexChanged.connect(self.zoomtosel)

    def zoomtosel(self):
        codcom = ""
        fpath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath, "r")
        testo = in_file.readlines()
        comune = ""
        codsez = ''
        if (self.ui.cat_com.currentText()) != comune:
            for ctcom in testo:
                line = ctcom.split(",")

                if line[3].strip() == self.ui.cat_com.currentText():
                    # print line[0].strip()
                    codcom = line[0].strip()

                    if line[1].strip() == '':
                        codsez = "_"
                    else:
                        codsez = line[1].strip()

        layer = QgsProject.instance().mapLayersByName("Particelle")[0]
        iface.setActiveLayer(layer)
        # iter= layer.getFeatures()
        # nfile = layer.fieldNameIndex('Nomefile')
        # map = layer.fieldNameIndex('Mappale')
        # sub= layer.fieldNameIndex('Denom')

        layer.removeSelection()
        foglio = codcom + codsez + self.ui.cat_fg.currentText()[2:255].replace("_", "")
        if self.ui.cat_mapp.currentText().find("-") != -1:
            map = self.ui.cat_mapp.currentText().split("-")
            # print (u'"Nomefile" = \''+foglio+'\' and "Mappale" =\''+ map[0]+'\' and "Denom" =\''+ map[1]+'\'')
            selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(
                u'"Nomefile" = \'' + foglio + '\' and "Mappale" =\'' + map[0] + '\' and "Denom" =\'' + map[1] + '\''))
        else:
            # print (u'"Nomefile" = \'' + foglio + '\' and "Mappale" =\'' + self.ui.cat_mapp.currentText() + '\'')
            selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(
                u'"Nomefile" = \'' + foglio + '\' and "Mappale" =\'' + self.ui.cat_mapp.currentText() + '\''))
        layer.select([k.id() for k in selection])
        iface.actionZoomToSelected().trigger()
        # if codsez == "":
        #     codsez = "_"
        # else:
        #     codsez = ""
        # for feature in iter:
        #  if   feature.attributes()[map] :
        #      print "k"
        #  print feature.attributes()[map]
        #      #"(feature.attributes()[map]+"-"+feature.attributes()[sub])
        #  #if feature.attributes()[nfile]==codcom+self.ui.cat_fg.currentText().replace ('_','') and feature.attributes()[map]+"-"+feature.attributes()[sub] ==self.ui.cat_mapp.currentText() :
        #  if feature.attributes()[nfile]==codcom+self.ui.cat_fg.currentText().replace ('_','') and feature.attributes()[map] ==self.ui.cat_mapp.currentText() :
        #
        #    layer.select( feature.id())
        #    iface.actio
        #    ZoomToSelected().trigger()
