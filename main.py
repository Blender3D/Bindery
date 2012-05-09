#!/usr/bin/env python

import sys, os, warnings, glob

with warnings.catch_warnings():
  warnings.simplefilter('ignore')

  from PyQt4.QtCore import *
  from PyQt4.QtGui import *

  import functions

try:
  from djvubind import utils
except:
  from binding.djvubind import utils

from thumbnailer import Thumbnailer
from previewer import Previewer

from binding.binder import Binder
from functionality import sorting, dialogs, error

from ui import gui, project_files, resources_rc, BookListWidget, ImageViewerWidget

class Bindery(sorting.Sorting, dialogs.Dialogs, error.Error, functions.Bindery, QMainWindow):
  name = 'Bindery'
  version = '2.7.4'
  caption = ''
  full_name = ' '.join([name, version, caption])
  description = 'Bindery is a cross-platform solution to binding scanned pages into PDF and DjVu documents.'
  
  def __init__(self, parent = None):
    QMainWindow.__init__(self, parent)
    
    self.settings = QSettings(' '.join([self.name, self.version]), 'Blender3D ')
    
    self.ui = gui.Ui_MainWindow()
    self.ui.setupUi(self)
    
    self.setWindowTitle(self.full_name)
    self.previews = True
    
    self.projectFiles = QDialog(self)
    self.projectFiles.ui = project_files.Ui_ProjectFilesDialog()
    self.projectFiles.ui.setupUi(self.projectFiles)

    self.projectFiles.ui.browseButton1.clicked.connect(self.showFileDialog)
    self.projectFiles.ui.browseButton2.clicked.connect(self.showSaveDialog)
    self.projectFiles.ui.addToProjectButton.clicked.connect(self.addToProject)
    self.projectFiles.ui.removeFromProjectButton.clicked.connect(self.removeFromProject)
    self.projectFiles.ui.okButton.clicked.connect(self.projectFilesAccepted)
    
    self.projectFiles.ui.addToProjectButton.setIcon(self.QIconFromTheme('go-next'))
    self.projectFiles.ui.removeFromProjectButton.setIcon(self.QIconFromTheme('go-previous'))
    
    self.projectFiles.ui.browseButton1.setIcon(self.QIconFromTheme('document-save'))
    self.projectFiles.ui.browseButton2.setIcon(self.QIconFromTheme('document-save'))

    self.projectFiles.ui.okButton.setIcon(self.QIconFromTheme('dialog-ok'))
    self.projectFiles.ui.cancelButton.setIcon(self.QIconFromTheme('process-stop'))
    
    self.projectFiles.ui.selectAllButton1.setIcon(self.QIconFromTheme('gtk-select-all'))
    self.projectFiles.ui.selectAllButton2.setIcon(self.QIconFromTheme('gtk-select-all'))
    
    self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.addPageButton.setIcon(self.QIconFromTheme('list-add'))
    self.ui.removePageButton.setIcon(self.QIconFromTheme('list-remove'))
    
    self.ui.newMenuItem.setIcon(self.QIconFromTheme('document-new'))
    self.ui.openMenuItem.setIcon(self.QIconFromTheme('document-open'))
    self.ui.saveMenuItem.setIcon(self.QIconFromTheme('document-save'))
    self.ui.saveAsMenuItem.setIcon(self.QIconFromTheme('document-save-as'))
    self.ui.quitMenuItem.setIcon(self.QIconFromTheme('exit'))
    self.ui.helpMenuItem.setIcon(self.QIconFromTheme('help'))
    self.ui.aboutMenuItem.setIcon(self.QIconFromTheme('gtk-about'))
    
    self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.addPageMenuItem.setIcon(self.QIconFromTheme('list-add'))
    self.ui.removePageMenuItem.setIcon(self.QIconFromTheme('list-remove'))
    
    self.ui.moveToTopButton.setIcon(self.QIconFromTheme('go-top'))
    self.ui.moveUpButton.setIcon(self.QIconFromTheme('go-up'))
    self.ui.moveDownButton.setIcon(self.QIconFromTheme('go-down'))
    self.ui.moveToBottomButton.setIcon(self.QIconFromTheme('go-bottom'))
    
    self.ui.clearLogButton.setIcon(self.QIconFromTheme('gtk-clear'))
    self.ui.saveLogButton.setIcon(self.QIconFromTheme('document-save'))
    
    self.ui.outputFileBrowseButton.setIcon(self.QIconFromTheme('document-save'))
    
    self.ui.actionReload_Thumbnails.setIcon(self.QIconFromTheme('reload'))
    self.ui.actionAbout_Qt4.setIcon(self.QIconFromTheme('gtk-about'))
    
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
    
    self.checkDependencies()
    
    if '--test' in sys.argv:
      for image in sorted(glob.glob('tests/*.tif')):
        self.addFile(image)
        
        self.ui.outputFile.setText('/tmp/output.djvu')
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
    
    self.itemSelectionChanged()
    self.hideBackground()
    self.thumbnailer.start()
  
  def closeEvent(self, event):
    if self.binder.isRunning():
      if QMessageBox.question(self, 'Bindery', 'A book is currently binding. Are you sure you want to exit?', QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
        event.accept()
      else:
        event.ignore()
  
  def QIconFromTheme(self, name):
    if QIcon.hasThemeIcon(name):
      return QIcon.fromTheme(name)
    else:
      return QIcon(':/icons/{0}.png'.format(name))

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  bindery = Bindery()

  if '--debug' not in sys.argv:
    sys.stderr = bindery
    sys.stdout = bindery
    sys.excepthook = bindery.handleError
  
  bindery.show()
  
  sys.exit(app.exec_())
