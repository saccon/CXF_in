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


from qgis.core import *
from qgis.utils import iface

from .  import globals
import os


def liv(radice):
    lista = []
    for child in radice.children():
        if isinstance(child, QgsLayerTreeGroup):
            lista.append(child.name())
            lista.append(liv(child))
        elif isinstance(child, QgsLayerTreeLayer):
            lista.append(child)
    return lista
def db_view_all(self,lista):
        #print("all+lista"+lista)

        uri = QgsDataSourceUri()
        if self.testdb() and self.ui.postgis.isChecked():

            uri.setConnection(str(globals.line[0]),"5432",str(globals.line[1]),str(globals.line[2]),str(globals.line[3]))
        else:
            uri.setDatabase(globals.dbName)

        uri.setDataSource(globals.schema.replace(".",""),'particelle', 'geom')
        vl_part = QgsVectorLayer(uri.uri(), 'Particelle', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'fabbricati', 'geom')
        vl_ed = QgsVectorLayer(uri.uri(), 'Fabbricati', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'strade', 'geom')
        vl_st = QgsVectorLayer(uri.uri(), 'Strade', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'confine', 'geom')
        vl_conf = QgsVectorLayer(uri.uri(), 'Confine', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'acque', 'geom')
        vl_aq = QgsVectorLayer(uri.uri(), 'Acque', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'linee', 'geom')
        vl_linee = QgsVectorLayer(uri.uri(), 'Linee', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'simboli', 'geom')
        vl_point = QgsVectorLayer(uri.uri(), 'Simboli', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'testi', 'geom')
        vl_testo = QgsVectorLayer(uri.uri(), 'Testi', globals.datadb)
        uri.setDataSource(globals.schema.replace(".",""),'fiduciali', 'geom')
        vl_fidu = QgsVectorLayer(uri.uri(), 'Fiduciali', globals.datadb)




        vl_part.updateExtents()
        vl_ed.updateExtents()
        vl_st.updateExtents()
        vl_aq.updateExtents()
        vl_conf.updateExtents()
        vl_linee.updateExtents()
        vl_point.updateExtents()
        vl_testo.updateExtents()

        QgsProject.instance().addMapLayer(vl_part,False)
        QgsProject.instance().addMapLayer(vl_ed,False)
        QgsProject.instance().addMapLayer(vl_st,False)
        QgsProject.instance().addMapLayer(vl_conf,False)
        QgsProject.instance().addMapLayer(vl_aq,False)
        QgsProject.instance().addMapLayer(vl_linee,False)
        QgsProject.instance().addMapLayer(vl_point,False)
        QgsProject.instance().addMapLayer(vl_testo,False)
        QgsProject.instance().addMapLayer(vl_fidu,False)


        #if not liv(QgsProject.instance().layerTreeRoot()):
        grup=QgsProject.instance().layerTreeRoot().insertGroup(0, "Catasto")
        livelligruppofoglio=[vl_aq,vl_st,vl_conf,vl_part,vl_testo,vl_fidu,vl_ed,vl_point,vl_linee]
        for l in livelligruppofoglio:
           grup.insertLayer(0,  l)

        for parent in QgsProject.instance().layerTreeRoot().children():
                   if isinstance(parent, QgsLayerTreeGroup):
                       if parent.name() == "Catasto":
                           for layer in parent.children():
                               QgsProject.instance().mapLayer(layer.layerId()).setSubsetString(lista)

        db_view_change_style()
            
def db_view_change_style():

        dirstili = ""
        in_file =open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty', 'r')
        for line in in_file:
           if line[:4]=="att:":
            dirstili=line.split (":",2)[2].replace("\n","")
            if(os.path.exists(dirstili) ==False):
                dirstili=  os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/QML_Default'
        #print ("Uscita")
        in_file.close()

        #print ("livelli")

        catlayers = liv(QgsProject.instance().layerTreeRoot())
        #print (catlayers )
        if catlayers[0] == 'Catasto':
          for layer in catlayers[1]:
                        if layer.name() == "Particelle":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/part.qml')
                        elif layer.name() == "Fabbricati":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/fab.qml')
                        elif layer.name() == "Strade":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/strade.qml')
                        elif layer.name() == "Confine":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/conf.qml')
                        elif layer.name() == "Acque":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/acque.qml')
                        elif layer.name() == "Linee":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/linee.qml')
                        elif layer.name() == "Simboli":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/Simboli.qml')
                        elif layer.name() == "Testi":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/testo.qml')
                        elif layer.name() == "Fiduciali":
                            QgsProject.instance().mapLayer(layer.layerId()).loadNamedStyle(dirstili+'/fidu.qml')
        iface.mapCanvas().refresh()

def db_view_sel(self,lista):

    #print (lista)
    if lista == "Nomefile=='9999'":
        for parent in QgsProject.instance().layerTreeRoot().children():
            if isinstance(parent, QgsLayerTreeGroup):
                if parent.name() == "Catasto":
                    QgsProject.instance().layerTreeRoot().removeChildNode(parent)
    trovatogruppo=0
    if  QgsProject.instance().layerTreeRoot().children():
        #print("ggg")
        for parent in QgsProject.instance().layerTreeRoot().children():
            if isinstance(parent, QgsLayerTreeGroup):
                if parent.name()=="Catasto":
                    #print("ggg")
                    trovatogruppo=1
                    for layer in parent.children():
                        QgsProject.instance().mapLayer(layer.layerId()).setSubsetString(lista)

        if trovatogruppo==0:
            if lista != "Nomefile=='9999'":
                db_view_all(self, lista)

    else:
        if lista != "Nomefile=='9999'":
            db_view_all(self, lista)


