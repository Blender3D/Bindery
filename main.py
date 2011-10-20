#!/usr/bin/env python

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import functions, config

from thumbnailer import *
from previewer import *

from binding import binder

from ui import gui, project_files, resources_rc
from BookListWidget import *

class StartQT4(functions.StartQT4, QMainWindow):
  def __init__(self, parent = None):
    QWidget.__init__(self, parent)
    
    QIcon.setThemeName('elementary')
    
    self.previews = True
    
    self.config = config.config('options.ini')
    
    self.ui = gui.Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.projectFiles = QDialog()
    self.projectFilesUi = project_files.Ui_ProjectFilesDialog()
    self.projectFilesUi.setupUi(self.projectFiles)

    self.projectFilesUi.browseButton1.clicked.connect(self.showFileDialog)
    self.projectFilesUi.browseButton2.clicked.connect(self.showSaveDialog)
    self.projectFilesUi.addToProjectButton.clicked.connect(self.addToProject)
    self.projectFilesUi.removeFromProjectButton.clicked.connect(self.removeFromProject)
    self.projectFilesUi.okButton.clicked.connect(self.projectFilesAccepted)
    
    self.projectFilesUi.addToProjectButton.setIcon(QIcon.fromTheme('forward'))
    self.projectFilesUi.removeFromProjectButton.setIcon(QIcon.fromTheme('back'))
    
    
    
    self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
    self.ui.addPageButton.setIcon(QIcon.fromTheme('list-add', QIcon(':/icons/media-playback-start.png')))
    self.ui.removePageButton.setIcon(QIcon.fromTheme('list-remove', QIcon(':/icons/list-remove.png')))
    
    self.ui.newMenuItem.setIcon(QIcon.fromTheme('filenew'))
    self.ui.openMenuItem.setIcon(QIcon.fromTheme('fileopen'))
    self.ui.saveMenuItem.setIcon(QIcon.fromTheme('filesave'))
    
    self.ui.startBindingMenuItem.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
    self.ui.addPageMenuItem.setIcon(QIcon.fromTheme('list-add', QIcon(':/icons/media-playback-start.png')))
    self.ui.removePageMenuItem.setIcon(QIcon.fromTheme('list-remove', QIcon(':/icons/list-remove.png')))
    
    self.ui.moveToTopButton.setIcon(QIcon.fromTheme('top'))
    self.ui.moveUpButton.setIcon(QIcon.fromTheme('up'))
    self.ui.moveDownButton.setIcon(QIcon.fromTheme('down'))
    self.ui.moveToBottomButton.setIcon(QIcon.fromTheme('bottom'))
    
    self.ui.saveMenuItem.setEnabled(False)
    self.ui.startBindingMenuItem.setEnabled(False)
    self.ui.removePageMenuItem.setEnabled(False)
    
    
    
    self.thumbnailer = Thumbnailer(self.ui.pageList)
    self.previewer = Previewer()
    self.binder = binder.Binder()
    
    self.connect(self.thumbnailer, SIGNAL('makeIcon(int, QImage)'), self.makeIcon)
    self.connect(self.previewer, SIGNAL('previewPage(QImage)'), self.previewPage)    
    
    self.connect(self.binder, SIGNAL('updateProgress(int, QString)'), self.updateProgress)
    self.connect(self.binder, SIGNAL('updateBackground(int, QColor)'), self.updateBackground)
    self.connect(self.binder, SIGNAL('finishedBinding'), self.finishedBinding)
    self.connect(self.binder, SIGNAL('error(QString)'), self.error)
    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  myapp = StartQT4()
  myapp.show()
  sys.exit(app.exec_())
