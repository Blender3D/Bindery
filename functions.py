import sys, os, subprocess, time

from gui import *
from DropListWidget import * 
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
  
  
  
  def fileDropped(self, file):
    '''
    Handles a file drop. Also used when file is chosen via dialog.
    '''
    
    if file is list:
      f = str(file[-1])
    else:
      f = str(file)
    
    toAll = ''
    new = ''
    
    if os.path.splitext(f)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tga']:
      if f not in self.getChildren(self.ui.pageList, True):
        new = './djvu_backup/' + os.path.splitext(os.path.split(f)[1])[0] + '.tiff'
      
    elif os.path.splitext(f)[1][1:].lower() in ['tif', 'tiff']:
      new = str(f)
    
    if new != '':
      item = QtGui.QListWidgetItem(os.path.split(f)[1], self.ui.pageList)
      item.setStatusTip(f)
      
      self.hideBackground()
      self.repaint()
      
      self.thumbnailer.queue = list(set(self.thumbnailer.queue).union(set(f)))
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
    
    self.ui.statusBar.clearMessage()
    self.ui.statusBar.showMessage('Thumbnailing ' + os.path.split(str(item.statusTip()))[1], 500)
    
    self.ui.pageList.setCurrentItem(item)
  
  
  
  def hideBackground(self):
    '''
    Hides the background image of the main QListWidget when it obtains
    more than one item, or adds it again when the widget has zero items.
    '''
    
    if len(self.getChildren(self.ui.pageList, True)) > 0:
      self.ui.pageList.setStyleSheet(_fromUtf8(''))
    else:
      self.ui.pageList.setStyleSheet(_fromUtf8('QListView\n{\nbackground-image: url(\'./icons/go-down-big.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}\n\nQListView:hover\n{\nbackground-image: url(\'./icons/go-down-big-hover.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}'))
  
  
  
  def showFileDialog(self):
    '''
    Shows the 'File Selection' dialog and pipes the output into the
    'fileDropped()' function for processing.
    '''
    
    files = QtGui.QFileDialog.getOpenFileNames(self, self.trUtf8('Open file'), QtCore.QDir.currentPath(), self.trUtf8('Images (*.png *.tiff *.jpg *.jpeg *.bmp *.tif)'))

    for file in files:
      self.fileDropped(file)
  
  
  
  def removeItems(self):
    '''
    Removes the selected items from the main QListWidget.
    '''
    
    selected = self.ui.pageList.selectedItems()
    
    for item in selected:
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    self.hideBackground()
  
  
  
  def updateProgress(self, value):
    self.ui.progressBar.setValue(value)
  
  
  
  def startBinding(self):
    '''
    Starts binding the book. It's a huge task...
    '''
    
    self.pages = [str(item) for item in self.getChildren(self.ui.pageList, True)]
    
    if len(self.pages) == 0:
      QtGui.QMessageBox.warning(self, self.trUtf8('Warning'), self.trUtf8('There are no pages to process!'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
      
      return False
    
    self.outFile = QtGui.QFileDialog.getSaveFileName(self, self.trUtf8('Save file'), self.trUtf8(os.path.normpath(str(QtCore.QDir.currentPath() + '/Book.djvu'))), self.trUtf8('DjVu Document (*.djvu)'))
    
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
    
    #QtGui.QMessageBox.message(self, self.trUtf8('Message'), self.trUtf8('The book has been saved to \'' + os.path.split(self.outFile)[-1] + '\'.'), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
