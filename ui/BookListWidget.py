from PyQt4.QtCore import *
from PyQt4.QtGui import *

from binding import organizer

from ui import resources_rc

def QIconFromTheme(name):
  if QIcon.hasThemeIcon(name):
    return QIcon.fromTheme(name)
  else:
    return QIcon(':/icons/{0}.svg'.format(name))

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
      
      self.emit(SIGNAL('dropped(QStringList)'), links)
    else:
      event.ignore()


class BookListWidgetItem(QListWidgetItem, organizer.Page):
  def __init__(self, text='', filepath='', parent=None):    
    QListWidgetItem.__init__(self)
    organizer.Page.__init__(self, filepath)
    
    self.defaultIcon = True
    self.number = 0
    
    self.setText(text)
    self.setSizeHint(QSize(72, 72))
    self.resetIcon()
  
  def resetIcon(self):
    self.setIcon(QIconFromTheme('image-loading'))
    self.defaultIcon = True
  
  def removeIcon(self):
    self.setSizeHint(QSize(-1, 20))
    self.setIcon(QIcon())
    self.defaultIcon = True
