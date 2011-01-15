#!/usr/bin/env python

import sys, os

from PyQt4 import QtCore, QtGui

import functions

from thumbnailer import *
from bind import *

from gui import *
from BookListWidget import *

class StartQT4(functions.StartQT4, QtGui.QMainWindow):
  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    
    self.previews = True
    
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.thumbnailer = Thumbnailer(self.ui.pageList)
    self.binder = Binder()
    
    self.connect(self.thumbnailer, QtCore.SIGNAL('makeIcon(int, QImage)'), self.makeIcon)
    self.connect(self.binder, QtCore.SIGNAL('updateProgress(int, QString)'), self.updateProgress)
    self.connect(self.binder, QtCore.SIGNAL('updateBackground(int, QColor)'), self.updateBackground)
    self.connect(self.binder, QtCore.SIGNAL('finishedBinding'), self.finishedBinding)
    
    self.connect(self.ui.addPageButton, QtCore.SIGNAL('clicked()'), self.showFileDialog)
    self.connect(self.ui.removePageButton, QtCore.SIGNAL('clicked()'), self.removeItems)
    
    self.connect(self.ui.startButton, QtCore.SIGNAL('clicked()'), self.startBinding)
    
    self.connect(self.ui.filePreviewsMenuItem, QtCore.SIGNAL('toggled(bool)'), self.togglePreviews)
    
    self.connect(self.ui.pageList, QtCore.SIGNAL('itemSelectionChanged()'), self.itemSelectionChanged)
    self.connect(self.ui.pageNumber, QtCore.SIGNAL('valueChanged(int)'), self.pageNumberChanged)
    self.connect(self.ui.pageDPI, QtCore.SIGNAL('valueChanged(int)'), self.pageDPIChanged)

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  myapp = StartQT4()
  myapp.show()
  sys.exit(app.exec_())
