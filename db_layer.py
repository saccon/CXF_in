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
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.utils import iface
from qgis.gui import *
from .db_load_cxf import *
from .  import globals
import os


def db_load(self,file):

        print(file)
        if file =='':
            #print(os.getenv("HOME"))
            if os.path.exists(os.getenv("HOME")+'/workpath'):
               fpath = open(os.getenv("HOME")+'/workpath', 'r')
               read_path = fpath.read()
               fpath.close
            else:
                read_path ="."
            (filename, filter) = QFileDialog.getOpenFileNames(iface.mainWindow(),
                          "Seleziona un file cxf da caricare...",read_path,
                          "CXF files (*.cxf)",
                          "Filtro per selezione file")
            if len(filename)==0:
                  return

            fpath = open(os.getenv("HOME")+'/workpath', 'w')
            fpath.write(os.path.dirname(filename[0]))
            fpath.close
        else:

            filename=set([file])
        ocur = globals.ocon.cursor()
        for f in filename:

            liv=os.path.basename (os.path.splitext( str(f))[0])

            ocur.execute("SELECT distinct Nomefile from "+globals.schema+"particelle where Nomefile='"+liv[0:11]+"'")
            if ocur.rowcount > 0:
                ocur.execute("delete from "+globals.schema+"particelle where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"fabbricati where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"strade where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"confine where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"acque where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"linee where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"simboli where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"testi where Nomefile='"+liv[0:11]+"'")
                ocur.execute("delete from "+globals.schema+"fiduciali where Nomefile='"+liv[0:11]+"'")
                globals.ocon.commit()
                if globals.postgis== "2":
                    old_isolation_level = globals.ocon.isolation_level
                    globals.ocon.set_isolation_level(0)
                    ocur = globals.ocon.cursor()
                    ocur.execute("VACUUM")
                    globals.ocon.set_isolation_level(old_isolation_level)
                else:
                    ocur.execute("VACUUM")
                
            load_cxf(self,str(f),liv,ocur,globals.ocon)

        globals.ocon.commit()

        ocur.close() 