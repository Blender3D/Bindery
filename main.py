#!/usr/bin/env python

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import functions, config

from thumbnailer import Thumbnailer
from previewer import Previewer

from binding.binder import Binder

from ui import gui, project_files, resources_rc, BookListWidget, DebugLog, ImageViewerWidget

class StartQT4(functions.StartQT4, QMainWindow):
  def __init__(self, parent = None):
    QMainWindow.__init__(self, parent)
    
    self.version = 'Bindery 2.7.0 (Beta PDF)'
    self.config = config.config('options.ini')
    
    self.ui = gui.Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.setWindowTitle(self.version)
    
    self.log = self.ui.debugLog
    
    
    self.projectFiles = QDialog(self)
    self.projectFilesUi = project_files.Ui_ProjectFilesDialog()
    self.projectFilesUi.setupUi(self.projectFiles)

    self.projectFilesUi.browseButton1.clicked.connect(self.showFileDialog)
    self.projectFilesUi.browseButton2.clicked.connect(self.showSaveDialog)
    self.projectFilesUi.addToProjectButton.clicked.connect(self.addToProject)
    self.projectFilesUi.removeFromProjectButton.clicked.connect(self.removeFromProject)
    self.projectFilesUi.okButton.clicked.connect(self.projectFilesAccepted)
    
    self.projectFilesUi.addToProjectButton.setIcon(self.QIconFromTheme('go-next'))
    self.projectFilesUi.removeFromProjectButton.setIcon(self.QIconFromTheme('go-previous'))
    
    
    self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.addPageButton.setIcon(self.QIconFromTheme('list-add'))
    self.ui.removePageButton.setIcon(self.QIconFromTheme('list-remove'))
    
    self.ui.newMenuItem.setIcon(self.QIconFromTheme('document-new'))
    self.ui.openMenuItem.setIcon(self.QIconFromTheme('document-open'))
    self.ui.saveMenuItem.setIcon(self.QIconFromTheme('document-save'))
    
    self.ui.insertBlankPageMenuItem.setIcon(self.QIconFromTheme('document-new'))
    
    self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.addPageMenuItem.setIcon(self.QIconFromTheme('list-add'))
    self.ui.removePageMenuItem.setIcon(self.QIconFromTheme('list-remove'))
    
    self.ui.moveToTopButton.setIcon(self.QIconFromTheme('go-top'))
    self.ui.moveUpButton.setIcon(self.QIconFromTheme('go-up'))
    self.ui.moveDownButton.setIcon(self.QIconFromTheme('go-down'))
    self.ui.moveToBottomButton.setIcon(self.QIconFromTheme('go-bottom'))
    
    self.ui.saveMenuItem.setEnabled(False)
    self.ui.startBindingMenuItem.setEnabled(False)
    self.ui.removePageMenuItem.setEnabled(False)
    
    
    self.thumbnailer = Thumbnailer(self.ui.pageList)
    self.previewer = Previewer()
    self.binder = Binder()
    
    self.connect(self.thumbnailer, SIGNAL('makeIcon(int, QImage)'), self.makeIcon)
    self.connect(self.previewer, SIGNAL('previewPage(QImage)'), self.previewPage)    
    
    self.connect(self.binder, SIGNAL('updateProgress(int, QString)'), self.updateProgress)
    self.connect(self.binder, SIGNAL('updateBackground(int, QColor)'), self.updateBackground)
    self.connect(self.binder, SIGNAL('finishedBinding'), self.finishedBinding)
    self.connect(self.binder, SIGNAL('error(QString)'), self.error)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
    
  def QIconFromTheme(self, name):
    if QIcon.hasThemeIcon(name):
      self.log.log('Loading icon (theme): {0}'.format(name))
      return QIcon.fromTheme(name)
    else:
      self.log.log('Loading icon (fallback): {0}'.format(name))
      return QIcon(':/icons/{0}.svg'.format(name))

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  bindery = StartQT4()
  bindery.show()
  
  sys.exit(app.exec_())
