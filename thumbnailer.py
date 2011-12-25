from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Thumbnailer(QThread):
  def __init__(self, ListWidget, parent = None):
    super(Thumbnailer, self).__init__(parent)
    
    self.widget = ListWidget
    self.running = False
    self.die = False
  
  def run(self):
    self.running = True
    
    for i in range(self.widget.count()):
      item = self.widget.item(i)
      
      if item.defaultIcon and not self.die:
        icon = QImage(item.filepath).scaled(800, 600, aspectRatioMode = Qt.KeepAspectRatio).scaled(72, 72, aspectRatioMode = Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        
        self.emit(SIGNAL('makeIcon(int, QImage)'), i, icon)
        item.defaultIcon = False
      elif self.die:
        for j in range(self.widget.count()):
          self.widget.item(j).removeIcon()
        
        break
    
    self.running = False
