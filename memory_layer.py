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

from PyQt5.QtGui import *
from PyQt5.QtCore import *

from qgis.core import *
from qgis.utils import iface
from qgis.gui import *
from .load_cxf_memory  import *
import os

def memory_layer(self,filename):



        selcrs=QgsProjectionSelectionDialog()
        result=selcrs.exec_()
        stringacrs="crs="+selcrs.crs().authid()
        if  result!=1 :
            QMessageBox.information(None, "Errore :","Selezione un CRS") 
            return   
        #print (stringacrs)
        
             
        del selcrs


        vl_conf= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double","Confine", "memory")
                         
        vl_part = QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Particelle", "memory")  
                         
        vl_ed= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Fabbricati", "memory")  
        vl_st= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Strade", "memory")  
        vl_aq= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Acque", "memory")  
        vl_linee= QgsVectorLayer("Linestring?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=Cod_linea:string(5)",
                           "Linee", "memory")
        vl_point= QgsVectorLayer("Point?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=Simbolo:string(5)&field=Rot:Double",
                           "Simboli", "memory")  
        vl_txt= QgsVectorLayer("Point?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=testo:string(50)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Testi", "memory")
        vl_fidu= QgsVectorLayer("Point?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=Codice:string(50)&field=Simbolo:string(5)&field=PosX:Double&field=PosY:Double&field=RelPosX:Double&field=RelPosY:Double",
                           "Fiduciali", "memory")
        livelligruppofoglio=[vl_aq,vl_st,vl_conf,vl_part,vl_txt,vl_fidu,vl_ed,vl_point,vl_linee]
        QgsProject.instance().addMapLayers(livelligruppofoglio,False)
        #if not liv(QgsProject.instance().layerTreeRoot()):
        grup = QgsProject.instance().layerTreeRoot().insertGroup(0, "Catasto_memory")
        livelligruppofoglio = [vl_aq, vl_st, vl_conf, vl_part, vl_txt, vl_fidu, vl_ed, vl_point, vl_linee]
        for l in livelligruppofoglio:
            grup.insertLayer(0, l)
        dirstili = ""
        in_file =open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/setting.sty', 'r')
        for line in in_file:
           if line[:4]=="att:":
            dirstili=line.split (":",2)[2].replace("\n","")
            if(os.path.exists(dirstili) ==False):
                dirstili=  os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/QML_Default'
        #print ("Uscita")
        in_file.close()
        vl_linee.loadNamedStyle(dirstili+'/linee.qml')
        vl_point.loadNamedStyle(dirstili+'/simboli.qml')
        vl_ed.loadNamedStyle(dirstili+'/fab.qml')
        vl_part.loadNamedStyle(dirstili+'/part.qml')
        vl_conf.loadNamedStyle(dirstili+'/conf.qml')
        vl_aq.loadNamedStyle(dirstili+'/acque.qml')
        vl_st.loadNamedStyle(dirstili+'/strade.qml')
        vl_txt.loadNamedStyle(dirstili+'/testo.qml')
        vl_fidu.loadNamedStyle(dirstili+'/fidu.qml')
        fpath = open(os.getenv("HOME")+'/workpath', 'w') 
        fpath.write(os.path.dirname(filename[0])) 
        fpath.close  
              
              
              
              
        for f in filename:        
            liv=os.path.basename (os.path.splitext( str(f))[0])
            load_cxf(self,str(f),liv,vl_aq,vl_st,vl_conf,vl_part,vl_txt,vl_fidu,vl_ed,vl_point,vl_linee)

        vl_part.commitChanges()
        vl_ed.commitChanges()
        vl_st.commitChanges()
        vl_aq.commitChanges() 
        vl_conf.commitChanges()
        vl_linee.commitChanges()
        vl_point.commitChanges()
        vl_txt.commitChanges()
        vl_fidu.commitChanges() 
        
        # li = QgisInterface.legendInterface()
        # index=li.addGroup(liv[0:10],False)
        #
        # for l in livelligruppofoglio:
        #     li.moveLayer(l, index)



