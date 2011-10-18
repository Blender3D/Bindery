#!/usr/bin/env python

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import functions
import config

from thumbnailer import *
from bind import *

import project_files
from gui import *
from BookListWidget import *

class StartQT4(functions.StartQT4, QMainWindow):
  def __init__(self, parent = None):
    QWidget.__init__(self, parent)
    
    self.previews = True
    self.outFile = None
    
    self.config = config.config('options.ini')
    
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.thumbnailer = Thumbnailer(self.ui.pageList)
    self.binder = Binder()
    
    self.connect(self.thumbnailer, SIGNAL('makeIcon(int, QImage)'), self.makeIcon)
    self.connect(self.thumbnailer, SIGNAL('debug(QString)'), self.debug)
    
    self.connect(self.binder, SIGNAL('updateProgress(int, QString)'), self.updateProgress)
    self.connect(self.binder, SIGNAL('updateBackground(int, QColor)'), self.updateBackground)
    self.connect(self.binder, SIGNAL('finishedBinding'), self.finishedBinding)
    self.connect(self.binder, SIGNAL('debug(QString)'), self.debug)
    
    self.connect(self.ui.addPageButton, SIGNAL('clicked()'), self.showProjectDialog)
    self.connect(self.ui.removePageButton, SIGNAL('clicked()'), self.removeItems)
    
    self.connect(self.ui.startButton, SIGNAL('clicked()'), self.startBinding)
    
    self.connect(self.ui.filePreviewsMenuItem, SIGNAL('toggled(bool)'), self.togglePreviews)
    
    self.connect(self.ui.pageList, SIGNAL('itemSelectionChanged()'), self.itemSelectionChanged)
    self.connect(self.ui.pageGrayscale, SIGNAL('stateChanged(int)'), self.pageGrayscaleChanged)
    
    self.projectFiles = QDialog()
    self.projectFilesUi = project_files.Ui_ProjectFilesDialog()
    self.projectFilesUi.setupUi(self.projectFiles)
    
    self.connect(self.projectFilesUi.browseButton1, SIGNAL('clicked()'), self.showFileDialog)
    self.connect(self.projectFilesUi.browseButton2, SIGNAL('clicked()'), self.showSaveDialog)
    self.connect(self.projectFilesUi.addToProjectButton, SIGNAL('clicked()'), self.addToProject)
    self.connect(self.projectFilesUi.removeFromProjectButton, SIGNAL('clicked()'), self.removeFromProject)
    self.connect(self.projectFilesUi.okButton, SIGNAL('clicked()'), self.projectFilesAccepted)
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  myapp = StartQT4()
  myapp.show()
  sys.exit(app.exec_())
