import sys, os, subprocess, time

from gui import *
from DropListWidget import * 
from thumbnailer import *

from PIL import Image
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class StartQT4(QtGui.QMainWindow):
  def getChildren(self, element, statusTip = False):
    children = []
    
    for i in range(element.count()):
      if not statusTip:
        children.append(element.item(i).text())
      else:
        children.append(element.item(i).statusTip())
    
    return children
  
  
  
  def fileDropped(self, file):
    if file is list:
      f = str(file[-1])
    else:
      f = str(file)
    
    toAll = ''
    new = ''
    
    if os.path.splitext(f)[1][1:].lower() in ['jpg', 'jpeg', 'bmp', 'png', 'tga']:
      '''
      if toAll != None:
        reply = QtGui.QMessageBox.question(self, 'Message', 'All files must be TIFF images. Would you like me to convert a copy of your file to the TIFF format?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.YesToAll | QtGui.QMessageBox.NoToAll, QtGui.QMessageBox.YesToAll)
        
        toAll = None
      
      if reply == QtGui.QMessageBox.Yes:       toAll = ''
      if reply == QtGui.QMessageBox.No:        toAll = ''
      if reply == QtGui.QMessageBox.YesToAll:  toAll = True
      if reply == QtGui.QMessageBox.NoToAll:   toAll = False
      
      if reply == QtGui.QMessageBox.Yes or toAll == True:
        if not os.path.exists('./djvu_backup/'):  os.mkdir('./djvu_backup/')
        
        if f not in self.getChildren(self.ui.pageList):
          new = './djvu_backup/' + os.path.splitext(os.path.split(f)[1])[0] + '.tiff'
          Image.open(f).save(new)
      
      elif reply == QtGui.QMessageBox.No or toAll == False:
        return False
      '''
      
      if f not in self.getChildren(self.ui.pageList, True):
        new = './djvu_backup/' + os.path.splitext(os.path.split(f)[1])[0] + '.tiff'
      
    elif os.path.splitext(f)[1][1:].lower() in ['tif', 'tiff']:
      new = str(f)
    
    if new != '':
      item = QtGui.QListWidgetItem(os.path.split(f)[1], self.ui.pageList)
      item.setStatusTip(f)
      
      self.hideBackground()
      self.repaint()
      
      if not self.thread.running:
        self.thread.images = list(set(self.thread.images).union(set(f)))
        self.thread.process()
  
  
  
  def makeIcon(self, index, image):
    item = self.ui.pageList.item(index)
    pixmap = QtGui.QPixmap(72, 72)
    pixmap.convertFromImage(image)
    icon = QtGui.QIcon(pixmap)
    item.setIcon(icon)
    
    self.ui.statusBar.clearMessage()
    self.ui.statusBar.showMessage('Thumbnailing ' + os.path.split(str(item.statusTip()))[1])
    
    self.ui.pageList.setCurrentItem(item)
  
  
  
  def hideBackground(self):
    if len(self.getChildren(self.ui.pageList, True)) > 0:
      self.ui.pageList.setStyleSheet(_fromUtf8(''))
    else:
      self.ui.pageList.setStyleSheet(_fromUtf8('QListView\n'
      '{\n'
      'background-image: url(\'./icons/go-down-big.png\');\n'
      'background-position: center;\n'
      'background-repeat: no-repeat;\n'
      'background-color: white;\n'
      '}\n'
      '\n'
      'QListView:hover\n'
      '{\n'
      'background-image: url(\'./icons/go-down-big-hover.png\');\n'
      'background-position: center;\n'
      'background-repeat: no-repeat;\n'
      'background-color: white;\n'
      '}'))
  
  
  
  def showFileDialog(self):
    files = QtGui.QFileDialog.getOpenFileNames(self, self.trUtf8('Open file'), QtCore.QString('~'), self.trUtf8('Images (*.png *.tiff *.jpg *.jpeg *.bmp *.tif)'))

    for file in files:
      self.fileDropped(file)
  
  
  
  def removeItems(self):
    selected = self.ui.pageList.selectedItems()
    
    for item in selected:
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    self.hideBackground()
  
  
  
  def startBinding(self):
    pages = []
    
    if self.ui.enableOCR.checkState() == 0:
      ocr = False
    else:
      ocr = True
    
    pages = [str(item) for item in self.getChildren(self.ui.pageList, True)]
    
    print pages
