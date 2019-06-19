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

from PyQt4.QtGui import *
from PyQt4.QtCore import *  
from qgis.core import *
from qgis.utils import iface
from qgis.gui import *
from pyspatialite import dbapi2 as sqlite3
from db_load_cxf  import *
from cercacatdialog import *
from .  import globals
import os


def db_delete_fg(QtGui):

        uri = QgsDataSourceURI()
        uri.setDatabase(globals.dbName)
        uri.setDataSource('','Particelle', 'geom')                          
        vl_part = QgsVectorLayer(uri.uri(), 'Particelle', 'spatialite')   
        uri.setDataSource('','Fabbricati', 'geom')  
        vl_ed = QgsVectorLayer(uri.uri(), 'Fabbricati', 'spatialite')
        uri.setDataSource('','Strade', 'geom')
        vl_st = QgsVectorLayer(uri.uri(), 'Strade', 'spatialite')
        uri.setDataSource('','Confine', 'geom') 
        vl_conf = QgsVectorLayer(uri.uri(), 'Confine', 'spatialite')
        uri.setDataSource('','Acque', 'geom')
        vl_aq = QgsVectorLayer(uri.uri(), 'Acque', 'spatialite')
        uri.setDataSource('','Linee', 'geom')
        vl_linee = QgsVectorLayer(uri.uri(), 'Linee', 'spatialite')
        uri.setDataSource('','Simboli', 'geom')
        vl_point = QgsVectorLayer(uri.uri(), 'Simboli', 'spatialite')
        uri.setDataSource('','Testi', 'geom')
        vl_testo = QgsVectorLayer(uri.uri(), 'Testi', 'spatialite')
        uri.setDataSource('','Fiduciali', 'geom')
        vl_fidu = QgsVectorLayer(uri.uri(), 'Fiduciali', 'spatialite')      
        layers = QgsMapLayerRegistry.instance().mapLayers() 
        
        
   
        #ocon = sqlite3.connect(globals.dbName)
        ocur = globals.ocon.cursor()
        ret=QMessageBox.question(None,"ATTENZIONE", codcom  ,QMessageBox.Yes, QMessageBox.No)
        ret = QMessageBox.question(None,"ATTENZIONE", "Vuoi veramente cancellare il foglio "+QtGui.ui.del_cat_fg.currentText()+" del Comune "+QtGui.ui.del_cat_com.currentText(),QMessageBox.Yes, QMessageBox.No)
        codcom =""
        
        fpath =os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/CTCOMCAT.txt'
        in_file = open(fpath,"r")        
        testo= in_file.readlines()
        comune=""   
        #print (self.ui.del_cat_com.currentText())
        if (self.ui.del_cat_com.currentText()) !=comune:   
           for ctcom in testo:
                line=ctcom.split(",")
                
                if line[3].strip()==self.ui.del_cat_com.currentText():
                      #print line[0].strip()
                      codcom=line[0].strip()    
        QMessageBox.question(None,"ATTENZIONE", codcom  ,QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.Yes:
            
          ocur.execute("delete from "+globals.schema+"particelle where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"fabbricati where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"strade where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"confine where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"acque where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"linee where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"simboli where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"testi where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
          ocur.execute("delete from "+globals.schema+"fiduciali where Codice_comune='"+codcom+"' and  Fg='"+self.ui.del_cat_fg.currentText()+"'")
#
#           vl_ed.updateExtents()
#           vl_st.updateExtents()
#           vl_aq.updateExtents()
#           vl_conf.updateExtents()
#           vl_linee.updateExtents()
#           vl_point.updateExtents()
#           vl_testo.updateExtents()

        if globals.postgis=="0":
              globals.ocon.isolation_level = None
              print ("vacuum")
              ocur.execute('VACUUM;')
              globals.ocon.isolation_level = ''
              globals.ocon.commit()
        else:
              globals.ocon.commit()
              ocur.execute('end transaction;')
              ocur.execute('VACUUM;')


        ocur.close() 