import sys, os, time

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
  '''
  Extension of main StartQT4 class
  '''
  
  def getChildren(self, element, statusTip = False):
    '''
    Returns a list of text or tooltips of the children of a QListWidget
    '''
    
    children = []
    
    for i in range(element.count()):
      if not statusTip:
        children.append(element.item(i).text())
      else:
        children.append(element.item(i).statusTip())
    
    return children
  
  
  
  def itemSelectionChanged(self):
    self.selected = self.ui.pageList.selectedItems()
    
    if len(self.selected) == 1:
      self.ui.pageNumber.setEnabled(True)
      self.ui.pageDPI.setEnabled(True)
      
      self.selected = self.selected[0]
      
      if self.selected.number is not None:  self.ui.pageNumber.setValue(self.selected.number)
      if self.selected.dpi is not None:  self.ui.pageDPI.setValue(self.selected.dpi)
    else:
      self.ui.pageNumber.setEnabled(False)
      self.ui.pageDPI.setEnabled(False)
  
  
  
  def pageNumberChanged(self, value):
    self.ui.pageList.selectedItems()[0].number = value
  
  
  def pageDPIChanged(self, value):
    self.ui.pageList.selectedItems()[0].dpi = value
  
  
  
  
  def fileAdded(self, files):
    '''
    Handles a file drop. Also used when file is chosen via dialog.
    '''
    
    for f in files:
      f = str(f)
      
      if os.path.splitext(f)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tga', 'tif', 'tiff']:
        if f not in self.getChildren(self.ui.pageList, True):
          item = BookListWidgetItem(os.path.split(f)[1], self.previews, self.ui.pageList)
          item.setStatusTip(f)
          
          self.hideBackground()
    
    if not self.thumbnailer.running and self.previews:
      self.thumbnailer.start()
      
  
  
  def makeIcon(self, index, image):
    '''
    Sets the icon of the QListWidgetIcon at the given index.
    '''
    
    item = self.ui.pageList.item(index)
    pixmap = QtGui.QPixmap(72, 72)
    pixmap.convertFromImage(image)
    icon = QtGui.QIcon(pixmap)
    item.setIcon(icon)
    
    self.ui.statusBar.showMessage('Thumbnailing ' + os.path.split(str(item.statusTip()))[1], 500)
  
  
  
  def hideBackground(self):
    '''
    Hides the background image of the main QListWidget when it obtains
    more than one item, or adds it again when the widget has zero items.
    '''
    
    if len(self.getChildren(self.ui.pageList, True)) > 0:
      self.ui.pageList.setStyleSheet(_fromUtf8(''))
    else:
      self.ui.pageList.setStyleSheet(_fromUtf8('QListWidget\n{\nbackground-image: url(\'./icons/go-down-big.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}\n\nQListWidget:hover\n{\nbackground-image: url(\'./icons/go-down-big-hover.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}'))
  
  
  
  def showFileDialog(self):
    '''
    Shows the 'File Selection' dialog and pipes the output into the
    'fileAdded()' function for processing.
    '''
    
    files = QtGui.QFileDialog.getOpenFileNames(self, self.trUtf8('Open file'), QtCore.QDir.currentPath(), self.trUtf8('Images (*.png *.tiff *.jpg *.jpeg *.bmp *.tif)'))

    self.fileAdded(files)
  
  
  
  def removeItems(self):
    '''
    Removes the selected items from the main QListWidget.
    '''
    
    selected = self.ui.pageList.selectedItems()
    
    for item in selected:
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    self.hideBackground()
  
  
  
  def togglePreviews(self, on = True):
    self.previews = on
    
    if on:
      self.thumbnailer.die = False
      
      for i in range(self.ui.pageList.count()):
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
    self.ui.progressBar.setValue(0)
    
    QtGui.QMessageBox.information(self, self.trUtf8('Message'), self.trUtf8('The book has been succesfully saved!'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    for i in range(self.ui.pageList.count()):
      self.ui.pageList.item(i).setBackground(QtGui.QColor(0, 0, 0, 0))
  
  
  def startBinding(self):
    '''
    Starts binding the book. It's a huge task...
    '''
    if str(self.ui.startButton.text()) == 'Start':
      self.pages = [str(item) for item in self.getChildren(self.ui.pageList, True)]
      
      if len(self.pages) == 0:
        QtGui.QMessageBox.warning(self, self.trUtf8('Warning'), self.trUtf8('There are no pages to process!'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        
        return False
      
      self.outFile = QtGui.QFileDialog.getSaveFileName(self, self.trUtf8('Save file'), self.trUtf8(os.path.normpath(str(QtCore.QDir.currentPath() + '/Book.djvu'))), self.trUtf8('DjVu Document (*.djvu)'))
      
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
