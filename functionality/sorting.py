from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Sorting(QMainWindow):
  def moveItemToTop(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(0, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(0)
  
  
  
  def moveItemUp(self):
    asd
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(currentRow - 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(currentRow - 1 if currentRow != 0 else 0)
  
  
  
  def moveItemDown(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(currentRow + 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(currentRow + 1 if currentRow != self.ui.pageList.count() - 1 else self.ui.pageList.count() - 1) 
  
  
  
  def moveItemToBottom(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(self.ui.pageList.count() - 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(self.ui.pageList.count() - 1)
