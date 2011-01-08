from PyQt4 import QtCore, QtGui

class DropListWidget(QtGui.QListWidget):
  def __init__(self, type, parent = None):
    super(DropListWidget, self).__init__(parent)
    
    self.setDragEnabled(True)
    self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
    self.setAlternatingRowColors(True)
    self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.setIconSize(QtCore.QSize(72, 72))
    self.setMovement(QtGui.QListView.Snap)
  
  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls:
      event.accept()
    else:
      event.ignore()

  def dragMoveEvent(self, event):
    if event.mimeData().hasUrls:
      event.setDropAction(QtCore.Qt.CopyAction)
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.mimeData().hasUrls:
      event.setDropAction(QtCore.Qt.CopyAction)
      event.accept()
      
      links = []
      
      for url in event.mimeData().urls():
        links.append(str(url.toLocalFile()))
        self.emit(QtCore.SIGNAL('dropped'), links)
      else:
        event.ignore()
