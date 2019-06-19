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
from .trasfcoord import *
import time
 
import sys
import math
import os
import string
import ntpath


def load_cxf(self,filename,liv,vl_aq,vl_st,vl_conf,vl_part,vl_txt,vl_fidu,vl_ed,vl_point,vl_linee):

  try:
      in_file = open(filename,"r")
  except IOError:
      print ('Impossibile aprire il file', filename)
      sys.exit()
      
  def dispoint(livello,codice ):
        geometria=[]
        simbolo= in_file.readline().strip()
        angolo= in_file.readline().strip()
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip()) 
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        sgeometria="point ("+str(x)+" "+str(y)+")"
         
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                     
                     (liv[9:10]),
                     (liv[10:11]), 
                     (simbolo),        
                     (math.degrees(float(angolo)))

                ]            
        feature.setAttributes(values)        
        vl_point.addFeature(feature,QgsFeatureSink.FastInsert)
        vl_point.updateExtents()
        

  def distext(livello,codice ):
        geometria=[]
        
        testo= in_file.readline().strip()
        dimensione= in_file.readline().strip()
        angolo= in_file.readline().strip()
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip()) 
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]        
        sgeometria="point ("+str(x)+" "+str(y)+")"
         
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (testo),
                     (float(dimensione)),

                     
                     (math.degrees(float(angolo))),
                                        
                     (float(x)),
                     (float(y)) ]
                      
        feature.setAttributes(values)        
        vl_txt.addFeature(feature,QgsFeatureSink.FastInsert)
        vl_txt.updateExtents()
        
        
        
  def disfidu(livello,codice ):
        geometria=[]
        
        numero= in_file.readline().strip()
        idenum= in_file.readline().strip()
        
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip())
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        orig1=[x,y]
        relx=float(in_file.readline().strip())
        rely=float(in_file.readline().strip()) 
        gauss=converti(self,foglio.metodo,rely,relx)
        relx=gauss[0]
        rely=gauss[1]
        orig1=[relx,rely]
        
        sgeometria="point ("+str(x)+" "+str(y)+")"
         
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (numero),
                     (idenum),

                     
                     (float(x)),
                     (float(y)),
                                        
                     (float(relx)),
                     (float(rely)) ]
                      
        feature.setAttributes(values)        
        vl_fidu.addFeature(feature,QgsFeatureSink.FastInsert)
        vl_fidu.updateExtents()

        
        
        
  def dislinee(livello,codice ):

        geometria=[]
        lt_testo  = in_file.readline().strip()      
        vert=int(in_file.readline().strip())
        sgeometria="Linestring ("
        for n in range (0,vert):
                 
                  x=float(in_file.readline().strip())
                  y=float(in_file.readline().strip()) 
                  gauss=converti(self,foglio.metodo,y,x)
                  x=gauss[0]
                  y=gauss[1]
                  geom= coord=[x,y]
                  if n == vert-1:
                    sgeometria=sgeometria+str(x)+" "+str(y)+")"
                  else:
                    sgeometria=sgeometria+str(x)+" "+str(y)+","
                

        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (float(lt_testo)),
]
        feature.setAttributes(values)        
        vl_linee.addFeature(feature,QgsFeatureSink.FastInsert)
        vl_linee.updateExtents()        
        
        
  def disarea(livello,codice ):

        geometria=[]
        area=[]
        lt_testo  = in_file.readline().strip()
        angolo  = in_file.readline().strip()

        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip())
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        orig1=[x,y]
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip())
        gauss=converti(self,foglio.metodo,y,x)
        x=gauss[0]
        y=gauss[1]
        orig2=[x,y]

        nrisole=int(in_file.readline().strip())
        nrverttot=int(in_file.readline().strip())
        #if nrisole > 0 :
        nrvertisola=[]

        for x in range(1,nrisole+1):
            nrvertisola.append(int(in_file.readline()))
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))

        sgeometria="POLYGON"
        for isola,vert in enumerate(nrvertisola):
              sgeometria=sgeometria+"("
              for n in range (0,vert):
                  x=float(in_file.readline().strip())
                  y=float(in_file.readline().strip()) 
                  gauss=converti(self,foglio.metodo,y,x)
                  x=gauss[0]
                  y=gauss[1]
                  geom= coord=[x,y]
                  if n == vert-1:
                    if isola==nrisole+1:
                        sgeom=str(x)+" "+str(y)+")"
                    else:
                        sgeom=str(x)+" "+str(y)+"),"
                  else:
                    sgeom=str(x)+" "+str(y)+","
                  sgeometria=sgeometria+sgeom
                  geometria.append(coord)
              area.append(geometria)
        sgeometria=sgeometria+")" 
        
        if codice=="726" :
         QMessageBox.information(None, "Avviso :","Utente riconosciuto"+str(sgeometria)) 
        
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (float(lt_testo)),
                     (math.degrees(float(angolo))),
                     (float(orig1[0])),
                     (float(orig1[1]))]
        if livello=="Acque":          
           feature.setAttributes(values)  
           vl_aq.addFeature(feature,QgsFeatureSink.FastInsert)
           vl_aq.updateExtents()   
        if livello=="Confine":          
           feature.setAttributes(values)   
           vl_conf.addFeature(feature,QgsFeatureSink.FastInsert)
           vl_conf.updateExtents()     
        if livello=="Strade":
           feature.setAttributes(values)  
           vl_st.addFeature(feature,QgsFeatureSink.FastInsert)
           vl_st.updateExtents()
           
        if livello=="FABBRICATI":
              
            feature.setAttributes(values)       
            vl_ed.addFeature(feature,QgsFeatureSink.FastInsert)
            vl_ed.updateExtents()   
            vl_ed.updateExtents()   
            vl_ed.updateExtents()   
           
             
        if livello=="Particelle":

           feature.setAttributes(values)
           vl_part.addFeature(feature,QgsFeatureSink.FastInsert)
           
           vl_part.updateFields()  
           vl_part.updateExtents() 
       
           if (orig1[0] != orig2[0]) and (orig1[1] != orig2[1]):
              sgeometria="Linestring ("+str(orig1[0])+" "+str(orig1[1])+","+str(orig2[0])+" "+str(orig2[1])+")"      
              feature = QgsFeature()
              feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
              values = [(liv[0:4]),
                           (liv[5:9]),
                           (codice),                      
                           (liv[9:10]),
                           (liv[10:11]),
                           (float(lt_testo)),
      ]
              feature.setAttributes(values)        
              vl_linee.addFeature(feature,QgsFeatureSink.FastInsert)
              vl_linee.updateExtents()   
        
            


    
  file =ntpath.split(filename)[1]


  


  foglio.metodo=""
    
  vl_part.startEditing()
  vl_ed.startEditing()
  vl_st.startEditing()
  vl_aq.startEditing()
  vl_conf.startEditing()
  vl_linee.startEditing()
  vl_point.startEditing()
  vl_txt.startEditing()
  vl_fidu.startEditing()
  while True:
    in_line= in_file.readline().strip()
    if in_line == "":
        break

    if in_line in  ("MAPPA","QUADRO D\'UNIONE"):
       mappa = in_file.readline().strip()
       
       if in_line == 'QUADRO D\'UNIONE':
        mappa = "QU"
       scala=in_file.readline().strip()

    elif in_line == 'BORDO':
        in_line  = in_file.readline().strip()
        if in_line[len(in_line)-1] == '+':
            disarea('FABBRICATI',in_line)
        elif in_line  == 'STRADA':
            disarea('Strade',in_line)
        elif in_line  == 'ACQUA':
            disarea('Acque',in_line)
        elif in_line  == mappa:
            disarea('Confine',in_line)
        elif mappa=="QU":
            disarea('Confine',in_line)            
        elif len(in_line) == 11 :
            disarea('Sezioni',in_line)
        else:
            disarea('Particelle',in_line)
    if in_line == "LINEA" :
            dislinee("Linee",in_line) 
    if in_line == "SIMBOLO" :
            dispoint("Simboli",in_line)
    if in_line == "LINEA\\" :
            dislinee("Linee",in_line)
    if in_line == "SIMBOLO\\" :
            dispoint("Simboli",in_line)
    if in_line == "TESTO" :
            distext("Testi",in_line)
    if in_line == "TESTO\\" :
            distext("Testi",in_line)
    if in_line == "FIDUCIALE" :
            disfidu("Fiduciali",in_line)
    if in_line == "FIDUCIALE\\" :
            disfidu("Fiduciali",in_line)                                                   
  in_file.close()