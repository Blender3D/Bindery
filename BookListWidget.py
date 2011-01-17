from PyQt4 import QtCore, QtGui

class BookListWidget(QtGui.QListWidget):
  def __init__(self, type, parent = None):
    super(BookListWidget, self).__init__(parent)
    
    self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.setDragEnabled(True)
    self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
    self.setAcceptDrops(True)
    self.setDropIndicatorShown(True)
    self.setAlternatingRowColors(True)
    self.setIconSize(QtCore.QSize(72, 72))

class BookListWidgetItem(QtGui.QListWidgetItem):
  def __init__(self, text = '', defaultIcon = True, parent = None):
    super(BookListWidgetItem, self).__init__(parent)
    self.defaultIcon = True
    
    self.number = 9
    self.dpi = None
    
    self.pixmap = QtGui.QPixmap(72, 72)
    self.pixmap.convertFromImage(QtGui.QImage('./icons/blank.png'))
    self.icon = QtGui.QIcon(self.pixmap)
    self.blank = QtGui.QIcon(QtGui.QPixmap(0, 0))
    
    self.setText(text)
    
    if defaultIcon:
      self.setIcon(self.icon)
  
  def resetIcon(self):
    self.setIcon(self.icon)
    self.defaultIcon = True
  
  def removeIcon(self):
    self.setIcon(self.blank)
    self.defaultIcon = True
