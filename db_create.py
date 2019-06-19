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
from qgis.utils import *
from qgis.gui import *
# import sqlite3
from . import globals


def db_create(self):
    ocur = globals.ocon.cursor()
    globals.ocon.commit()
    CRS = ""
    if self.ui.postgis.isChecked():
        try:
            ocur.execute('create schema cxf_in')
            globals.ocon.commit()
        except:
            pass
    globals.ocon.commit()
    try:
        if self.ui.postgis.isChecked():
            globals.ocon.commit()
            ocur.execute("select srid from geometry_columns where f_table_schema='cxf_in' and f_table_name='particelle'")
            globals.ocon.commit()
        else:
            ocur.execute("SELECT distinct(auth_srid) FROM 'geom_cols_ref_sys' where f_table_name='particelle' ")
            globals.ocon.commit()
        for d in ocur:
            CRS = str(d[0])
    except:
        pass

    if self.ui.postgis.isChecked():
        dimensione = '2'
        schema = "'" + globals.schema.replace(".", "") + "',"
        sql = 'Id BIGSERIAL NOT NULL PRIMARY KEY ,'
        schema = "'" + schema.replace(".", "',")
    else:
        dimensione = "'XY'"
        sql = 'Id INTEGER NOT NULL PRIMARY KEY ,'
        schema = ""

    if CRS == "":
        selcrs = QgsProjectionSelectionDialog()
        result = selcrs.exec_()
        if result == 1:
            CRS = selcrs.crs().authid().split(':', 1)[1]
        else:
            return

    globals.ocon.commit()

    sql += 'Codice_comune varchar(4),'
    sql += 'Sez varchar(1),'
    sql += 'Fg varchar(4),'
    sql += 'Mappale varchar(11),'
    sql += 'Denom varchar(5),'
    sql += 'Allegato varchar(1),'
    sql += 'Svi varchar(1),'
    sql += 'Nomefile varchar(11),'
    sql += 'Ext varchar(1),'
    schemanodot = globals.schema.replace(".", "")

    try:
        if (globals.postgis == "0"):
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'particelle (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real,supcat real)')
            ocur.execute("SELECT AddGeometryColumn('particelle','geom'," + CRS + ", 'POLYGON'," + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'confine (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('confine','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"fabbricati" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('fabbricati','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"strade" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('strade','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"acque" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('acque','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"linee" (' + sql + 'Cod_linea varchar(5))')
            ocur.execute("SELECT AddGeometryColumn('linee','geom'," + CRS + ", 'LINESTRING', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"simboli" (' + sql + 'Simbolo varchar(5),Rot real)')
            ocur.execute("SELECT AddGeometryColumn('simboli','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"testi" (' + sql + 'Testo varchar(50),Dim real,Rot real)')
            ocur.execute("SELECT AddGeometryColumn('testi','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"fiduciali" (' + sql + 'Codice varchar(50),Simbolo varchar(5),PosX real,PosY real, RelPosX real,RelPosY real)')
            ocur.execute("SELECT AddGeometryColumn('fiduciali','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'selezione (' + sql.split(",")[0] + ',Codice_comune varchar(5),Comune varchar(50),Sez varchar(1),Fg varchar(10),Nomefile varchar(11),Sel varchar(1))')
            globals.ocon.commit()
        else:
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'particelle (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real,supcat real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','particelle','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'confine (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','confine','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"fabbricati" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','fabbricati','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"strade" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','strade','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"acque" (' + sql + 'Htxt real,Rtxt real,Xtxt real,Ytxt real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','acque','geom'," + CRS + ", 'POLYGON', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"linee" (' + sql + 'Cod_linea varchar(5))')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','linee','geom'," + CRS + ", 'LINESTRING', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"simboli" (' + sql + 'Simbolo varchar(5),Rot real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','simboli','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"testi" (' + sql + 'Testo varchar(50),Dim real,Rot real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','testi','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + '"fiduciali" (' + sql + 'Codice varchar(50),Simbolo varchar(5),PosX real,PosY real, RelPosX real,RelPosY real)')
            ocur.execute("SELECT AddGeometryColumn('" + schemanodot + "','fiduciali','geom'," + CRS + ", 'POINT', " + dimensione + ")")
            globals.ocon.commit()
            # print 'CREATE TABLE if not exists ' + schema + 'selezione ('+sql+'Codice_comune varchar(5),Comune varchar(50),Fg varchar(5),Nomefile varchar(11),Sel varchar(1))'
            ocur.execute('CREATE TABLE if not exists ' + globals.schema + 'selezione (' + sql.split(",")[0] + ',Codice_comune varchar(5),Comune varchar(50),Sez varchar(1),Fg varchar(10),Nomefile varchar(11),Sel varchar(1))')
            globals.ocon.commit()

    except:
        ocur.close()

    ocur.close()
    globals.ocon.commit()
