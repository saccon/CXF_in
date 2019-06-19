# -*- coding: latin1 -*-
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
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from qgis.core import *
from qgis.utils import iface
from qgis.gui import *
from .trasfcoord import *
from .  import globals
#from pyspatialite import dbapi2 as sqlite3
import math
import ntpath

def load_cxf(self,filename,liv,ocur,ocon):
  global contariga
  try:
      in_file = open(filename, "r", encoding="utf8", errors='ignore')
      in_sup = open(ntpath.splitext(filename)[0] + ".sup","r")
      supfile=True
  except IOError:
      supfile=False
      print ('Impossibile aprire il file', filename)
      ret = QMessageBox.question(None, "ATTENZIONE ", 'Impossibile aprire il file SUP /n continua senza superfici catastali', QMessageBox.Yes)
      #sys.exit()
      
  def dispoint(self,livello,codice ):
        global contariga
        geometria=[]
        simbolo= in_file.readline().strip()
        contariga+=1
        angolo= in_file.readline().strip()
        contariga+=1
        x=float(in_file.readline().strip())
        contariga+=1
        y=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        esterno=""
        if codice[-1:]=="\\" :
          esterno = "1"
          codice=codice[:-1]
        sgeometria="point ("+str(x)+" "+str(y)+")"
        sql = "INSERT INTO "+globals.schema+"simboli (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Ext,Simbolo,Rot,geom) VALUES  ("
        sql +="'"+ liv[0:4] + "','" + liv[4:5] + "','" + liv[5:9] + "','" + codice[0:4] + "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]+ "','" + esterno
        sql +="','"+simbolo+"','"+str(math.degrees(float(angolo)))+"',"          
        sql +=globals.funzsql+"('"+ sgeometria+"',"+str(CRS)+"))"
        ocur.execute(sql)
                              
  def disfidu(self,livello,codice ):
        global contariga
        geometria=[]
        numero= in_file.readline().strip()
        contariga+=1
        idenum= in_file.readline().strip()
        contariga+=1
        x=float(in_file.readline().strip())
        contariga+=1
        y=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        relx=float(in_file.readline().strip())
        contariga+=1
        rely=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,rely,relx)
        relx=gauss[0]
        rely=gauss[1] 
        esterno=""
        if codice[-1:]=="\\" :
          esterno = "1"
          codice=codice[:-1]
        sgeometria="point ("+str(x)+" "+str(y)+")"
        sql = "INSERT INTO "+globals.schema+"fiduciali (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Ext,Codice,Simbolo,PosX,PosY,RelPosX,RelPosY,geom) VALUES  ("
        sql +="'"+ liv[0:4] +"','" + liv[4:5] + "','" + liv[5:9] + "','" + codice[0:4] + "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]+ "','" + esterno
        sql +="','"+numero+"','"+idenum+"','"+str(float(x))+"','" +str(float(y))+"','" +str(float(relx))+"','" +str(float(rely))+"',"          
        sql +=globals.funzsql+"('"+ sgeometria+"',"+str(CRS)+"))"
        ocur.execute(sql)
                 
  def distesto(self,livello,codice ):
        global contariga

        geometria=[]
        testo= in_file.readline().strip()
        contariga+=1
        dim= in_file.readline().strip()
        contariga+=1
        angolo= in_file.readline().strip()
        contariga+=1
        x=float(in_file.readline().strip())
        contariga+=1
        y=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]   
        esterno=""
        if codice[-1:]=="\\" :
          esterno = "1"
          codice=codice[:-1]
        testo =  testo.replace("'","''")
        sgeometria="point ("+str(x)+" "+str(y)+")"
        sql = "INSERT INTO "+globals.schema+"testi (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Ext,Testo,Dim,Rot,geom) VALUES  ("
        sql +="'"+ liv[0:4] +"','" + liv[4:5] + "','" + liv[5:9] + "','" + codice[0:4] + "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]+ "','" + esterno
        sql +="','"+testo+"','"+str(float(dim)*float(scala)/10000)+"','"+str(math.degrees(float(angolo)))+"',"          
        sql +=globals.funzsql+"('"+ sgeometria+"',"+str(CRS)+"))"
        ocur.execute(sql)
                                           
                                             
  def dislinee(self,livello,codice ):
        global contariga
        geometria=[]
        lt_testo  = in_file.readline().strip()
        contariga+=1
        vert=int(in_file.readline().strip())
        contariga+=1
        sgeometria="Linestring ("
        for n in range (0,vert):
                  x=float(in_file.readline().strip())
                  contariga+=1
                  y=float(in_file.readline().strip())
                  contariga+=1
                  gauss=converti(self,foglio.metodo,y,x)
                  x=gauss[0]
                  y=gauss[1]
                  geom= coord=[x,y]
                  if n == vert-1:
                    sgeometria=sgeometria+str(x)+" "+str(y)+")"
                  else:
                    sgeometria=sgeometria+str(x)+" "+str(y)+","   
        esterno=""
        if codice[-1:]=="\\" :
              esterno = "1"
              codice=codice[:-1]
        sql = "INSERT INTO "+globals.schema+"linee (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Ext,Cod_linea,geom) VALUES  ("
        sql +="'"+ liv[0:4] + "','" + liv[4:5] +"','" + liv[5:9] + "','" + codice[0:4] + "','" + liv[9:10] + "','" + liv[10:11]+ "','" + liv [0:11]+ "','" + esterno
        sql +="','"+lt_testo+"',"          
        sql +=globals.funzsql+"('"+ sgeometria+"',"+str(CRS)+"))"
        ocur.execute(sql)
                             

        
  def disarea(self,livello,codice ):
        global contariga
        geometria=[]
        area=[]
        lt_testo  = in_file.readline().strip()
        contariga+=1
        angolo  = in_file.readline().strip()
        contariga+=1
        x=float(in_file.readline().strip())
        contariga+=1
        y=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        orig1=[x,y]
        x=float(in_file.readline().strip())
        contariga+=1
        y=float(in_file.readline().strip())
        contariga+=1
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        orig2=[x,y]
        nrisole=int(in_file.readline().strip())
        contariga+=1
        nrverttot=int(in_file.readline().strip())
        contariga+=1
        nrvertisola=[]
        for x in range(1,nrisole+1):
            nrvertisola.append(int(in_file.readline()))
            contariga+=1
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))
        sgeometria="POLYGON"
        for isola,vert in enumerate(nrvertisola):
              sgeometria=sgeometria+"("
              for n in range (0,vert):
                  x=float(in_file.readline().strip())
                  contariga+=1
                  y=float(in_file.readline().strip())
                  contariga+=1
                  gauss=converti(self,foglio.metodo,y,x)
                  x=gauss[0]
                  y=gauss[1]
                  if n==0:
                      inix=x
                      iniy=y
                  geom= coord=[x,y]
                  if n == vert-1:
                    if isola==nrisole+1:
                        if abs(x-inix)<0.005:
                            x=inix
                        if abs(y-iniy)<0.005:
                            y=iniy
                        sgeom=str(x)+" "+str(y)+")"
                    else:
                        sgeom=str(x)+" "+str(y)+"),"
                  else:
                    sgeom=str(x)+" "+str(y)+","
                  sgeometria=sgeometria+sgeom
                  geometria.append(coord)
              area.append(geometria)
        sgeometria=sgeometria+")"        
        
        sup_cat_find=part_sup.get(codice.strip())
        if sup_cat_find==None:
            sup_cat_find='00'

                             
        if livello=="particelle":
            if codice.strip().find("/") != -1:
              if codice.strip().index("/")>0:
                denom=codice.strip().split("/")[1]
                mappale=codice.strip().split("/")[0]
                sql = "INSERT INTO " + globals.schema + livello + " (Codice_comune,Sez,Fg,Mappale,Denom,Allegato,Svi,Nomefile,Htxt,Rtxt,Xtxt,Ytxt,supcat,geom) VALUES  ("
                sql += "'" + liv[0:4] + "','" + liv[4:5] + "','" + liv[5:9] + "','" +mappale+"','" +denom+ "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]
                sql += "','" + lt_testo + "','" + angolo + "','" + str(float(orig1[0]) - 0.1) + "','" + str(float(orig1[1]) - 0.25) + "','" + sup_cat_find + "',"
                sql += globals.funzsql + "('" + sgeometria + "'," + str(CRS) + "))"
            else:
                sql = "INSERT INTO " + globals.schema + livello + " (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Htxt,Rtxt,Xtxt,Ytxt,supcat,geom) VALUES  ("
                sql += "'" + liv[0:4] + "','" + liv[4:5] + "','" + liv[5:9] + "','" + codice.strip() + "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]
                sql += "','" + lt_testo + "','" + angolo + "','" + str(float(orig1[0]) - 0.1) + "','" + str(float(orig1[1]) - 0.25) + "','" + sup_cat_find + "',"
                sql += globals.funzsql + "('" + sgeometria + "'," + str(CRS) + "))"

            ocur.execute(sql)
            if (orig1[0] !=  orig2[0]) and (orig1[1] !=  orig2[1]):
              sgeometria="Linestring ("+str(orig1[0])+" "+str(orig1[1])+","+str(orig2[0])+" "+str(orig2[1])+")"      
              sql = "INSERT INTO "+globals.schema+"linee (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Cod_linea,geom) VALUES  ("
              sql +="'"+ liv[0:4] + "','" + liv[4:5] +"','" + liv[5:9] + "','" + codice.strip() + "','" + liv[9:10] + "','" + liv[10:11]+ "','" + liv [0:11]
              sql +="','99',"          
              sql +=globals.funzsql+"('"+ sgeometria+"',"+str(CRS)+"))"
              ocur.execute(sql)
        else:
          if codice.strip().find("/")!=-1:
            if codice.strip().index("/") > 0:
                denom = codice.strip().split("/")[1]
                mappale = codice.strip().split("/")[0]
          sql = "INSERT INTO " + globals.schema + livello + " (Codice_comune,Sez,Fg,Mappale,Allegato,Svi,Nomefile,Htxt,Rtxt,Xtxt,Ytxt,geom) VALUES  ("
          sql += "'" + liv[0:4] + "','" + liv[4:5] + "','" + liv[5:9] + "','" + codice.strip() + "','" + liv[9:10] + "','" + liv[10:11] + "','" + liv[0:11]
          sql += "','" + lt_testo + "','" + angolo + "','" + str(float(orig1[0]) - 0.1) + "','" + str(float(orig1[1]) - 0.25) + "',"
          sql += globals.funzsql + "('" + sgeometria + "'," + str(CRS) + "))"

          ocur.execute(sql)
                       
  file =ntpath.split(filename)[1]

  globals.ocon.commit()


  if self.ui.postgis.isChecked():
      globals.ocon.commit()
      ocur.execute("select srid from geometry_columns where f_table_schema='cxf_in' and f_table_name='particelle'")
      globals.ocon.commit()
  else:
      ocur.execute("SELECT distinct(auth_srid) FROM 'geom_cols_ref_sys' where f_table_name='particelle' ")
      globals.ocon.commit()
  for d in ocur:
      CRS = str(d[0])



  setattr(foglio,"outcrs",CRS )
  tras_param(self,file)

  part_sup = {}
  
  if supfile:
      if self.ui.georef_db.isChecked()==False:
        foglio.metodo=""
      in_line = in_sup.readline()
      in_line = in_sup.readline()
      in_line = in_sup.readline()
      part = int(in_line[11:21].strip())
      in_line = in_sup.readline()
      in_line = in_sup.readline()
      in_line = in_sup.readline()
      in_line = in_sup.readline()

      for x in range(0, part):
          in_line = in_sup.readline()
          part_sup.update({in_line[0:11].strip(): in_line[11:21].strip()})
          if in_line == "":
              break
          if in_line == "N.PARTIC":
              break

  contariga = 0
  while True:
    in_line= in_file.readline().strip()
    contariga+=1
    print (contariga)
    if in_line == "":
        break
    if in_line == 'MAPPA':

       mappa = in_file.readline().strip()
       contariga+=1
       print(mappa)
       scala=in_file.readline().strip()
       contariga+=1
    elif in_line == 'MAPPA FONDIARIO':
        mappa = in_file.readline().strip()
        contariga+=1
        scala = in_file.readline().strip()
        contariga+=1
    elif in_line == 'QUADRO D\'UNIONE':
       mappa = "QU"
       scala=in_file.readline().strip()
       contariga+=1
    elif in_line == 'BORDO':
        in_line  = in_file.readline().strip()
        contariga+=1
        if in_line[len(in_line)-1] == '+':
            disarea(self,'fabbricati',in_line)
        elif in_line  == 'STRADA':
            disarea(self,'strade',in_line)
        elif in_line  == 'ACQUA':
            disarea(self,'acque',in_line)
        elif in_line  == mappa:
            disarea(self,'confine',in_line)
        elif mappa=="QU":
            disarea(self,'confine',in_line)
        elif len(in_line) == 11 :
            disarea(self,'sezioni',in_line)
        else:
            disarea(self,'particelle',in_line)
    elif in_line == "LINEA" :
            dislinee(self,"linee",in_line)
    elif in_line == "LINEA\\" :
            dislinee(self,"linee",in_line)
    elif in_line == "SIMBOLO" :
            dispoint(self,"simboli",in_line)
    elif in_line == "SIMBOLO\\" :
            dispoint(self,"simboli",in_line)
    elif in_line == "TESTO" :
            distesto(self,"testi",in_line)
    elif in_line == "TESTO\\" :
            distesto(self,"testi",in_line)
    elif in_line == "FIDUCIALE" :
            disfidu(self,"fiduciali",in_line)
    elif in_line == "FIDUCIALE\\" :
            disfidu(self,"fiduciali",in_line)
  in_file.close()