import os

from PIL import Image, ImageFilter
from PyQt4 import QtCore, QtGui

class Thumbnailer(QtCore.QThread):
  def __init__(self, ListWidget, parent = None):
    super(Thumbnailer, self).__init__(parent)
    self.widget = ListWidget
    self.running = False
    
    if not os.path.exists('./djvu_backup/'):  os.mkdir('./djvu_backup/')
    if not os.path.exists('./djvu_backup/thumbnails/'):  os.mkdir('./djvu_backup/thumbnails/')
  
  def run(self):
    self.running = True
    
    for i in range(self.widget.count()):
      item = self.widget.item(i)
      
      if item.defaultIcon:
        djvu_backup = './djvu_backup/' + os.path.splitext(os.path.split(str(item.statusTip()))[1])[0]
        thumbnail = './djvu_backup/thumbnails/' + os.path.splitext(os.path.split(str(item.statusTip()))[1])[0]
        
        Image.open(str(item.statusTip())).save(djvu_backup, 'TIFF')
        
        thumb_image = Image.open(str(item.statusTip()))
        thumb_image.thumbnail([72, 72])
        thumb_image.save(thumbnail, 'TIFF')
        
        icon = QtGui.QImage(thumbnail)
        
        self.emit(QtCore.SIGNAL('makeIcon(int, QImage)'), i, icon)
        item.defaultIcon = False
    
    self.running = False
