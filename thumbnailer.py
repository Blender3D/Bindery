import os

from PIL import Image, ImageFilter
from PyQt4 import QtCore, QtGui

class Thumbnailer(QtCore.QThread):
  def __init__(self, ListWidget, parent = None):
    super(Thumbnailer, self).__init__(parent)
    self.widget = ListWidget
    self.running = False
    self.die = False
    
    if not os.path.exists('./djvu_backup/'):  os.mkdir('./djvu_backup/')
    if not os.path.exists('./djvu_backup/thumbnails/'):  os.mkdir('./djvu_backup/thumbnails/')
  
  def run(self):
    self.running = True
    
    for i in xrange(self.widget.count()):
      item = self.widget.item(i)
      
      if item.defaultIcon and not self.die:
        djvu_backup = './djvu_backup/' + os.path.splitext(os.path.split(item.filepath)[1])[0]
        thumbnail = './djvu_backup/thumbnails/' + os.path.splitext(os.path.split(item.filepath)[1])[0]
        
        Image.open(item.filepath).save(djvu_backup, 'TIFF')
        
        thumb_image = Image.open(item.filepath)
        thumb_image.thumbnail([72, 72])
        thumb_image.save(thumbnail, 'TIFF')
        
        icon = QtGui.QImage(thumbnail)
        
        self.emit(QtCore.SIGNAL('makeIcon(int, QImage)'), i, icon)
        item.defaultIcon = False
      elif self.die:
        for j in xrange(self.widget.count()):
          self.widget.item(j).removeIcon()
        
        break
    
    self.running = False
