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
import os
import sys
import ntpath
import xml.etree.ElementTree as etree
from PyQt5.QtWidgets  import QMessageBox
import contextlib
import math
import urllib


class foglio(object):
    pass
class matrix(object):
    pass
class trasform(object):
    pass
def scala(origin, point, scalex,scaley):
    ox= float(origin[0])
    oy = float(origin[1])
    px, py = point

    qx = ((py-ox )*scalex)+ox
    qy = ((px -oy)*scaley)+oy
    return qx, qy

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox= float(origin[0])
    oy = float(origin[1])
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
def converti(self,trasf,x,y):
 if trasf=="e":
     return trasf_e(self,x,y)    
 elif trasf=="eAf":
     return trasf_eAF(self,x,y)   
 elif trasf=="eAfn":
     return trasf_eAFn(self,x,y)       
 elif trasf=="proj4":
     return trasf_proj4(self,x,y)
 elif trasf=="proj4evo":
     return trasf_proj4evo(self,x,y)
 else:    
     return (y,x)    
     
 
def trasf_e(self,x,y):
       tx = matrix.T1e +(matrix.Se *( (matrix.R1e * y) + (matrix.R2e * x) )  )
       ty = matrix.T2e +(matrix.Se *( (matrix.R2e * y) + (matrix.R1e * x) )  )
       return (tx,ty)
       
def trasf_eAF(self,x,y):
       tx = (matrix.T1e + ((matrix.SeX * (matrix.R1e - (matrix.R2e * matrix.Sband))) * y)) + ((matrix.SeX * (matrix.R2e + (matrix.R1e * matrix.Sband))) * x)
       ty = (matrix.T2e + ((matrix.SeY * -(matrix.R2e)) * y)) + ((matrix.SeY * matrix.R1e) * x)
       #return (tx,ty)
       geom = foglio.trasf.transform(QgsPointXY(tx, ty))
       return (geom.x(), geom.y())


def trasf_eAFn(self,x,y):
       tx = (matrix.T1e + ((matrix.SeX * (matrix.R1e - (matrix.R2e * matrix.Sband))) * y)) + ((matrix.SeX * (matrix.R2e + (matrix.R1e * matrix.Sband))) * x)
       ty = (matrix.T2e + ((matrix.SeY * -(matrix.R2e)) * y)) + ((matrix.SeY * matrix.R1e) * x)
       #print "-"+str(tx)
       gauss=foglio.trasf.transform(QgsPointXY(tx,ty))
       tx=gauss[0]
       #print str(tx)
       ty=gauss[1] 
           
          # print str(tx),str(ty)
       return (tx,ty)        
# def trasf_eAF(self,x,y):
#        tx = (matrix.T1e + ((matrix.SeX * (matrix.R1e - (matrix.R2e * matrix.Sband))) * y)) + ((matrix.SeX * (matrix.R2e + (matrix.R1e * matrix.Sband))) * x)
#        ty = (matrix.T2e + ((matrix.SeY * -(matrix.R2e)) * y)) + ((matrix.SeY * matrix.R1e) * x)
#        return (tx,ty)
def trasf_proj4(self,x,y):

    geom =foglio.trasf.transform(QgsPointXY(y,x))

    return (geom.x(),geom.y())
def trasf_proj4evoinvert(self, x, y):
    x,y=rotate(tuple(foglio.orig.split(",")),(y, x),float(foglio.rotang))
    x, y = scala(tuple(foglio.orig.split(",")), (y, x), float(foglio.scalex), float(foglio.scaley))
    geom = foglio.trasf.transform(QgsPointXY(x,y))

def trasf_proj4evo(self, x, y):
    x,y=rotate(tuple(foglio.orig.split(",")),(y, x),float(foglio.rotang))
    x, y = scala(tuple(foglio.orig.split(",")), (y, x), float(foglio.scalex), float(foglio.scaley))

    crsTemp = QgsCoordinateReferenceSystem(3003)
    trasf = QgsCoordinateTransform(foglio.incrs, crsTemp, QgsProject.instance())
    geomtemp = trasf.transform(QgsPointXY(x,y))
    #print(foglio.rotorig[0])
    x1,y1= (geomtemp.x() + float(foglio.traslx), geomtemp.y() + float(foglio.trasly))
    #return (x1,y1)
    crsDest = QgsCoordinateReferenceSystem(int(foglio.outcrs))
    trasf = QgsCoordinateTransform(crsTemp,crsDest, QgsProject.instance())
    geom = trasf.transform(QgsPointXY(x1, y1))
   # print(geom.x()+ matrix.traslx)
    return (geom.x() , geom.y())

def gaussovest(self, x, y):
        geom = foglio.trasf.transform(QgsPointXY(y, x))
        return (geom.x(), geom.y())

def tras_param(self,file):      

        if self.ui.etrs89_db.isChecked()==False:
            req='http://www.prgcloud.com/auth/gettransform.php?username='+self.ui.user.text()+'&password='+self.ui.password.text()+'&foglio='+file.split(".")[0]
        else:
            req='http://www.prgcloud.com/auth/gettransform.php?username='+self.ui.user.text()+'&password='+self.ui.password.text()+'&foglio='+file.split(".")[0]+'&trasf=3045'

        html=""
        print(req)
        try:
                with contextlib.closing(urllib.request.urlopen(req)) as x:
                  for line in x:
                      html=line.decode()
                      break
        except urllib.URLError as err:
                    QMessageBox.information(None, "Avviso :","Errore "+str(err)+file.split(".")[0]  )
                    return
        if html.strip()=="":
            QMessageBox.information(None, "Avviso :", "Errore trasf non trovata "+file.split(".")[0] )
            setattr(foglio, "foglio", file.split(os.extsep, 1)[0])
            setattr(foglio, "metodo", "")
            return

        while html.find("\n\n")>0:
            html=html.replace("\n\n","\n")
        docxml=(html.replace ("&lt;","<").replace("&gt;",">").replace("<br />","").replace("\r","").replace("\t",""))
        while docxml.find("\n\n")>0:
            docxml=docxml.replace("\n\n","\n")
        doc= etree.fromstring(docxml)
        ric_fg=file.split(os.extsep, 1)[0]
        for root in doc.findall("."):
            setattr(foglio,"foglio",ric_fg)
            for imp in root.find("./trasformazioneF"):
             if imp.tag!="Origine":
              setattr(foglio,imp.tag,imp.text)
        doc= etree.fromstring(docxml)
        for imp in doc.findall("./trasformazioneF/Origine/"):
                if imp.tag in ("codice","ValidoDa","ValidoA"):
                    setattr(matrix,imp.tag,imp.text)
                else:

                    setattr(matrix,imp.tag,float(imp.text))
        #if self.ui.etrs89_db.isChecked()==True:
        if foglio.metodo=="eAf":
              setattr(foglio,"metodo","eAfn")
              crsSrc = QgsCoordinateReferenceSystem(int(foglio.SRID))
              crsDest = QgsCoordinateReferenceSystem(int(foglio.outcrs))
              trasf=QgsCoordinateTransform(crsSrc,crsDest,QgsProject.instance())
              print ("in",str(foglio.SRID))
              setattr(foglio,"trasf",trasf)
              print ("out", foglio.outcrs)

        if foglio.metodo=="proj4":

            crsDest = QgsCoordinateReferenceSystem(int(foglio.outcrs))

            incrs = QgsCoordinateReferenceSystem()
            incrs.createFromProj4(foglio.SRID)
            setattr(foglio, "incrs", incrs)
            print (incrs.toWkt())
            print (crsDest.toWkt())

            trasf = QgsCoordinateTransform(incrs , crsDest,QgsProject.instance())
            setattr(foglio, "trasf", trasf)
        if foglio.metodo == "proj4evo":
            crsDest = QgsCoordinateReferenceSystem(int(foglio.outcrs))

            incrs = QgsCoordinateReferenceSystem()
            incrs.createFromProj4(foglio.SRID)
            setattr(foglio, "incrs", incrs)
            #print ("evo"+foglio.SRID,foglio.traslx,foglio.trasly)

            trasf = QgsCoordinateTransform(incrs, crsDest, QgsProject.instance())
            setattr(foglio, "trasf", trasf)
        if foglio.metodo=="gauss":

            crsDest = QgsCoordinateReferenceSystem(int(foglio.outcrs))

            incrs = QgsCoordinateReferenceSystem()
            incrs.createFromProj4(foglio.SRID)
            setattr(foglio, "incrs", incrs)
            print (incrs.toWkt())
            print (crsDest.toWkt())

            trasf = QgsCoordinateTransform(incrs, crsDest,QgsProject.instance())
            setattr(foglio, "trasf", trasf)
        if foglio.metodo == "":
            print("gauss")
        #     setattr(trasform, "PROJ4", QgsCoordinateTransform(foglio.incrs, foglio.outcrs))
        #





                