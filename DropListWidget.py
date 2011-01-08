from PyQt4 import QtCore, QtGui

class DropListWidget(QtGui.QListWidget):
  def __init__(self, type, parent = None):
    super(DropListWidget, self).__init__(parent)
    
    self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.setDragEnabled(True)
    self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
    self.setAcceptDrops(True)
    self.setDropIndicatorShown(True)
    self.setAlternatingRowColors(True)
    self.setIconSize(QtCore.QSize(72, 72))
    
  '''
  def dragEnterEvent(self, event):
    if event.source() == self:
      event.accept()
    elif event.mimeData().hasUrls:
      event.accept()
    else:
      event.ignore()

  def dragMoveEvent(self, event):
    if event.source() == self:
      event.accept()
    elif event.mimeData().hasUrls:
      event.setDropAction(QtCore.Qt.CopyAction)
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.source() == self:
      event.setDropAction(QtCore.Qt.MoveAction)
      event.accept()
      
      print event.mimeData().text()
    elif event.mimeData().hasUrls:
      event.setDropAction(QtCore.Qt.CopyAction)
      event.accept()
      
      links = []
      
      for url in event.mimeData().urls():
        links.append(str(url.toLocalFile()))
        self.emit(QtCore.SIGNAL('dropped'), links)
    else:
      event.ignore()
  '''
