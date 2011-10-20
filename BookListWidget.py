from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BookListWidget(QListWidget):
  def __init__(self, type, parent = None):
    super(BookListWidget, self).__init__(parent)
    
    self.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.setDragEnabled(True)
    self.setDragDropMode(QAbstractItemView.InternalMove)
    self.setAcceptDrops(True)
    self.setDropIndicatorShown(True)
    self.setAlternatingRowColors(True)
    self.setIconSize(QSize(72, 72))

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls:
      event.accept()
    else:
      event.ignore()

  def dragMoveEvent(self, event):
    if event.source() == self:
      event.setDropAction(Qt.MoveAction)
      event.accept()
    elif event.mimeData().hasUrls:
      event.setDropAction(Qt.CopyAction)
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.source() == self:
      event.setDropAction(Qt.MoveAction)
      event.ignore()
    elif event.mimeData().hasUrls:
      event.setDropAction(Qt.CopyAction)
      event.accept()
      
      links = []
      
      for url in event.mimeData().urls():
        links.append(str(url.toLocalFile()))
      
      self.emit(SIGNAL('dropped'), links)
    else:
      event.ignore()



class BookListWidgetItem(QListWidgetItem):
  def __init__(self, text = '', filepath = '', defaultIcon = True, parent = None):
    super(BookListWidgetItem, self).__init__(parent)
    self.defaultIcon = True
    
    self.number = 0
    self.dpi = 0
    self.grayscale = False
    
    self.icon = QIcon(QPixmap.fromImage(QImage(':/icons/blank.png')))
    self.blank = QIcon(QPixmap(72, 72))
    
    self.setText(text)
    self.filepath = filepath
    self.image = QImage(':/icons/blank.png')
    
    self.setSizeHint(QSize(72, 72))
    
    if defaultIcon:
      self.setIcon(self.icon)
  
  def resetIcon(self):
    self.setIcon(self.icon)
    self.defaultIcon = True
  
  def removeIcon(self):
    self.setIcon(self.blank)
    self.defaultIcon = True
