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
from qgis.gui import *



from .  import globals
def db_delete(self):
          ocur = globals.ocon.cursor()
          #print "aperto"
          #ocon = sqlite3.connect(globals.dbName)
          #ocur = ocon.cursor()
#           selcrs=QgsGenericProjectionSelector()
#           result=selcrs.exec_()     
#           if  result==1 :     
#               CRS=selcrs.selectedAuthId ().split(':',1)[1]                  
#           else:
#               QMessageBox.information(None, "Errore :","Selezione un CRS") 
#               return        
          if self.ui.postgis.isChecked():
              ocur.execute("drop schema cxf_in CASCADE")

          else:
              ocur.execute('drop TABLE if exists Particelle')
              ocur.execute('drop TABLE if exists Confine')
              ocur.execute('drop TABLE if exists Fabbricati')
              ocur.execute('drop TABLE if exists Strade')
              ocur.execute('drop TABLE if exists Acque')
              ocur.execute('drop TABLE if exists Linee')
              ocur.execute('drop TABLE if exists Simboli')
              ocur.execute('drop TABLE if exists Testi')
              ocur.execute('drop TABLE if exists Fiduciali')
              ocur.execute('drop TABLE if exists Selezione')


              ocur.execute("SELECT DiscardGeometryColumn('Particelle','geom') ")
              ocur.execute("SELECT DiscardGeometryColumn('Confine','geom' ) ")
              ocur.execute("SELECT DiscardGeometryColumn('Fabbricati','geom')  ")
              ocur.execute("SELECT DiscardGeometryColumn('Strade','geom')  ")
              ocur.execute("SELECT DiscardGeometryColumn('Acque','geom') ")
              ocur.execute("SELECT DiscardGeometryColumn('Linee','geom') ")
              ocur.execute("SELECT DiscardGeometryColumn('Simboli','geom')  ")
              ocur.execute("SELECT DiscardGeometryColumn('Testi','geom') ")
              ocur.execute("SELECT DiscardGeometryColumn('Fiduciali','geom') ")
              ocur.execute("SELECT DiscardGeometryColumn('Selezione','geom') ")

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

              #globals.ocon.commit()
          #ocur.execute('VACUUM')
          #globals.ocon.commit()

        