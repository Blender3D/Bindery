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
    self.outFile = None
    
    self.config = config.config('options.ini')
    
    self.ui = gui.Ui_MainWindow()
    self.ui.setupUi(self)
    
    
    
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
    
    self.connect(self.ui.pageList, SIGNAL('dropped'), self.filesDropped)
    self.connect(self.ui.pageList, SIGNAL('itemSelectionChanged()'), self.itemSelectionChanged)
    
    self.connect(self.ui.newMenuItem, SIGNAL('triggered()'), self.showProjectDialog)
    self.connect(self.ui.addPageMenuItem, SIGNAL('triggered()'), self.addFiles)
    
    self.connect(self.ui.addPageButton, SIGNAL('clicked()'), self.addFiles)
    self.connect(self.ui.removePageButton, SIGNAL('clicked()'), self.removeItems)
    
    self.connect(self.ui.moveToTopButton, SIGNAL('clicked()'), self.moveItemToTop)
    self.connect(self.ui.moveUpButton, SIGNAL('clicked()'), self.moveItemUp)
    self.connect(self.ui.moveDownButton, SIGNAL('clicked()'), self.moveItemDown)
    self.connect(self.ui.moveToBottomButton, SIGNAL('clicked()'), self.moveItemToBottom)
    
    self.connect(self.ui.startButton, SIGNAL('clicked()'), self.startBinding)
    self.connect(self.ui.startBindingMenuItem, SIGNAL('triggered()'), self.startBinding)
    
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
