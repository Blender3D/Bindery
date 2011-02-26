import sys, os, time, glob

import project_files
from gui import *
from BookListWidget import * 
from thumbnailer import *
from bind import *

from PIL import Image
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class StartQT4(QtGui.QMainWindow):
  def itemSelectionChanged(self):
    self.selected = self.ui.pageList.selectedItems()
    
    self.ui.pageGrayscale.setChecked(False)
    
    if len(self.selected) == 1:
      self.selected = self.selected[0]
      self.ui.tab.setEnabled(True)
      
      self.ui.pageGrayscale.setChecked(self.selected.grayscale)
      
      #self.ui.imageViewer.addImage(QtGui.QPixmap(self.selected.filepath))
    else:
      self.ui.tab.setEnabled(False)
  
  
  
  def pageGrayscaleChanged(self, state):
    self.ui.pageList.selectedItems()[0].grayscale = (state == 2)
  
  
  
  
  def fileAdded(self, files):
    for f in files:
      f = str(f)
      
      if os.path.splitext(f)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tga', 'tif', 'tiff']:
        if f not in [self.ui.pageList.item(i).filepath for i in xrange(self.ui.pageList.count())]:
          item = BookListWidgetItem(os.path.split(f)[1], f, self.previews, self.ui.pageList)
          
          self.hideBackground()
    
    if not self.thumbnailer.running and self.previews:
      self.thumbnailer.start()
      
  
  
  def makeIcon(self, index, image):
    item = self.ui.pageList.item(index)
    pixmap = QtGui.QPixmap.fromImage(image)
    icon = QtGui.QIcon(pixmap)
    item.setIcon(icon)
    
    self.ui.statusBar.showMessage('Thumbnailing ' + os.path.split(str(item.filepath))[1], 500)
  
  
  
  def hideBackground(self):
    if self.ui.pageList.count() > 0:
      self.ui.pageList.setStyleSheet(_fromUtf8(''))
    else:
      self.ui.pageList.setStyleSheet(_fromUtf8('QListWidget\n{\nbackground-image: url(\'./icons/go-down-big.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}\n\nQListWidget:hover\n{\nbackground-image: url(\'./icons/go-down-big-hover.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}'))
  
  
  
  def showProjectDialog(self):
    self.projectFiles.show()    



  def showFileDialog(self):
    directory = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8('Input directory'), QtCore.QDir.currentPath())
    
    self.projectFilesUi.inputDirectory.setText(str(directory) + '/')
    
    for file in glob.glob(str(directory) + '/*.*'):
      item = QtGui.QListWidgetItem(os.path.split(file)[-1])
      item.setStatusTip(file)
      
      if os.path.splitext(os.path.split(file)[-1])[-1] not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
        item.setFlags(QtCore.Qt.NoItemFlags)
      
      self.projectFilesUi.offProjectList.addItem(item)
    
    #self.fileAdded(files)
  
  
  
  def showSaveDialog(self):
    self.outFile = QtGui.QFileDialog.getSaveFileName(self, self.trUtf8('Save output file'), self.trUtf8(os.path.normpath(str(QtCore.QDir.currentPath() + '/Book.djvu'))), self.trUtf8('DjVu Document (*.djvu)'))
    self.projectFilesUi.outputFile.setText(self.outFile)

  
  def addToProject(self):
    for item in self.projectFilesUi.offProjectList.selectedItems():
      self.projectFilesUi.offProjectList.takeItem(self.projectFilesUi.offProjectList.row(item))
      self.projectFilesUi.inProjectList.addItem(item)


  
  def removeFromProject(self):
    for item in self.projectFilesUi.inProjectList.selectedItems():
      self.projectFilesUi.inProjectList.takeItem(self.projectFilesUi.inProjectList.row(item))
      self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def projectFilesAccepted(self):
    if self.projectFilesUi.inProjectList.count() == 0:
      QtGui.QMessageBox.warning(self, self.trUtf8('Warning'), self.trUtf8('There are no pages to process.\nPlease add them using the green arrows.'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    elif self.outFile in ['', None]:
      QtGui.QMessageBox.warning(self, self.trUtf8('Warning'), self.trUtf8('No output file has been selected.\nPlease select one using the "Output File" form.'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    else:
      self.projectFiles.close()
      
      for i in xrange(self.projectFilesUi.inProjectList.count()):
        orig = self.projectFilesUi.inProjectList.item(i)
        item = BookListWidgetItem(str(orig.text()), str(orig.statusTip()))
        
        self.ui.pageList.addItem(item)
      
      self.hideBackground()
      self.thumbnailer.start()
  
  def removeItems(self):
    for item in self.ui.pageList.selectedItems():
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    self.hideBackground()
  
  
  
  def debug(self, message):
    self.ui.debugLog.add(message)
  
  
  
  def togglePreviews(self, on = True):
    self.previews = on
    
    if on:
      self.thumbnailer.die = False
      
      for i in xrange(self.ui.pageList.count()):
        self.ui.pageList.item(i).resetIcon()
      
      self.thumbnailer.start()
    else:
      self.thumbnailer.die = True
  
  
  
  def updateProgress(self, value, message = None):
    self.ui.progressBar.setValue(value)
    self.ui.statusBar.showMessage(message)
  
  
  
  def updateBackground(self, item, color):
    self.ui.pageList.item(item).setBackground(color)
  
  
  
  def finishedBinding(self):
    self.ui.progressBar.reset()
    self.ui.statusBar.showMessage('Done binding the book!')
    
    self.ui.startButton.setText(QtCore.QString('Start'))
    startIcon = QtGui.QIcon()
    startIcon.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/media-playback-start.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.ui.startButton.setIcon(startIcon)
    
    QtGui.QMessageBox.information(self, self.trUtf8('Message'), self.trUtf8('The book has been succesfully saved!'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    self.ui.statusBar.clearMessage()
        
    for i in xrange(self.ui.pageList.count()):
      self.ui.pageList.item(i).setBackground(QtGui.QColor(0, 0, 0, 0))
  
  
  def startBinding(self):
    '''
    Starts binding the book. It's a huge task...
    '''
    if str(self.ui.startButton.text()) == 'Start':
      self.pages = [self.ui.pageList.item(i) for i in xrange(self.ui.pageList.count())]
    
      self.ui.startButton.setText(QtCore.QString('Stop'))
      stopIcon = QtGui.QIcon()
      stopIcon.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/media-playback-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.ui.startButton.setIcon(stopIcon)
      
      
      self.options = {'cores':             -1,
                      'ocr':               (self.ui.enableOCR.checkState() != 0),
                      'ocr_engine':        str(self.ui.ocrEngine.currentText()).lower(),
                      'cuneiform_options': str(self.ui.ocrOptions.text()),
                      'tesseract_options': str(self.ui.ocrOptions.text()),
                      'bitonal_encoder':   str(self.ui.bitonalEncoder.currentText()),
                      'color_encoder':     str(self.ui.colorEncoder.currentText()),
                      'c44_options':       str(self.ui.c44Options.text()),
                      'cjb2_options':      str(self.ui.cjb2Options.text()),
                      'cpaldjvu_options':  str(self.ui.cpaldjvuOptions.text()),
                      'csepdjvu_options':  str(self.ui.csepdjvuOptions.text()),
                      'minidjvu_options':  str(self.ui.minidjvuOptions.text()),
                      'numbering_type':    [],
                      'numbering_start':   [],
                      'win_path':          'C:\\Program Files\\DjVuZone\\DjVuLibre\\'}
      
      self.binder.initialize(self.pages, self.options, self.outFile)
      self.binder.start()
    else:
      self.binder.die = True
      self.ui.progressBar.reset()
      
      self.ui.startButton.setText(QtCore.QString('Start'))
      startIcon = QtGui.QIcon()
      startIcon.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/media-playback-start.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
      self.ui.startButton.setIcon(startIcon)
