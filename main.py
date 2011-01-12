#!/usr/bin/env python

import sys, os

from PyQt4 import QtCore, QtGui

import functions

from thumbnailer import *
from bind import *

from gui import *
from DropListWidget import *

class StartQT4(functions.StartQT4, QtGui.QMainWindow):
  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.pixmap = QtGui.QPixmap(72, 72)
    self.pixmap.convertFromImage(QtGui.QImage('./icons/blank.png'))
    self.icon = QtGui.QIcon(self.pixmap)
    
    self.thumbnailer = Thumbnailer(self.ui.pageList)
    self.binder = Binder()
    
    self.connect(self.ui.pageList, QtCore.SIGNAL('dropped'), self.fileDropped)
    self.connect(self.thumbnailer, QtCore.SIGNAL('makeIcon(int, QImage)'), self.makeIcon)
    self.connect(self.binder, QtCore.SIGNAL('updateProgress(int)'), self.updateProgress)
    
    self.connect(self.ui.addPageButton, QtCore.SIGNAL('clicked()'), self.showFileDialog)
    self.connect(self.ui.removePageButton, QtCore.SIGNAL('clicked()'), self.removeItems)
    
    self.connect(self.ui.startButton, QtCore.SIGNAL('clicked()'), self.startBinding)

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  myapp = StartQT4()
  myapp.show()
  sys.exit(app.exec_())
