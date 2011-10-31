#!/usr/bin/env python

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import functions, config

from thumbnailer import Thumbnailer
from previewer import Previewer

from binding import binder

from ui import gui, project_files, resources_rc, BookListWidget, DebugLog, ImageViewerWidget

def QIconFromTheme(name):
  if QIcon.hasThemeIcon(name):
    return QIcon.fromTheme(name)
  else:
    print 'Loading icon: {0}'.format(name)
    return QIcon(':/icons/{0}.svg'.format(name))

class StartQT4(functions.StartQT4, QMainWindow):
  def __init__(self, parent = None):
    QWidget.__init__(self, parent)
    
    #QIcon.setThemeName('elementary')
	
    self.previews = True
    self.config = config.config('options.ini')
    
    self.ui = gui.Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.projectFiles = QDialog(self)
    self.projectFilesUi = project_files.Ui_ProjectFilesDialog()
    self.projectFilesUi.setupUi(self.projectFiles)

    self.projectFilesUi.browseButton1.clicked.connect(self.showFileDialog)
    self.projectFilesUi.browseButton2.clicked.connect(self.showSaveDialog)
    self.projectFilesUi.addToProjectButton.clicked.connect(self.addToProject)
    self.projectFilesUi.removeFromProjectButton.clicked.connect(self.removeFromProject)
    self.projectFilesUi.okButton.clicked.connect(self.projectFilesAccepted)
    
    self.projectFilesUi.addToProjectButton.setIcon(QIconFromTheme('go-next'))
    self.projectFilesUi.removeFromProjectButton.setIcon(QIconFromTheme('go-previous'))
    
    
    
    self.ui.startButton.setIcon(QIconFromTheme('media-playback-start'))
    self.ui.addPageButton.setIcon(QIconFromTheme('list-add'))
    self.ui.removePageButton.setIcon(QIconFromTheme('list-remove'))
    
    self.ui.newMenuItem.setIcon(QIconFromTheme('document-new'))
    self.ui.openMenuItem.setIcon(QIconFromTheme('document-open'))
    self.ui.saveMenuItem.setIcon(QIconFromTheme('document-save'))
    
    self.ui.startBindingMenuItem.setIcon(QIconFromTheme('media-playback-start'))
    self.ui.addPageMenuItem.setIcon(QIconFromTheme('list-add'))
    self.ui.removePageMenuItem.setIcon(QIconFromTheme('list-remove'))
    
    self.ui.moveToTopButton.setIcon(QIconFromTheme('go-top'))
    self.ui.moveUpButton.setIcon(QIconFromTheme('go-up'))
    self.ui.moveDownButton.setIcon(QIconFromTheme('go-down'))
    self.ui.moveToBottomButton.setIcon(QIconFromTheme('go-bottom'))
    
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
