# -*- coding: utf-8 -*-
"""
/***************************************************************************
CARICA CXF 
                                 A QGIS plugin

                             -------------------
        begin                : 2012-09-13
        copyright            : (C) 2012 by Arch. Fabio Saccon
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
# Import the PyQt and QGIS libraries
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# Import the code for the dialog
from .catdialog import catDialog
import os.path
from .  import globals


class Cxf_in():



           
    def __init__(self, iface):
        self.iface = iface
        self.srs= ""
        self.crs=QgsCoordinateReferenceSystem()



    def initGui(self):
        self.pluginname = '&QGIS Importatore CXF  '
        self.action = QAction(QIcon(':/plugins/Cxf_in/icon.png'), self.pluginname, self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu('&CXF import', self.action)
        for action in self.iface.pluginMenu().actions():
            if (action.text() == self.pluginname):
                action.setIcon(QIcon(':/plugins/Cxf_in/icon.png'))




    def unload(self):
        self.iface.removePluginMenu('&CXF import', self.action)
        self.iface.removeToolBarIcon(self.action)



    # run method that performs all the real work
    def run(self):

        self.dockWidget = catDialog(self.iface)  
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)  

        
  
        
