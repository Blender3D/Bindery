import os

from PIL import Image, ImageFilter
from PyQt4 import QtCore, QtGui

class Thumbnailer(QtCore.QThread):
  def __init__(self, ListWidget, parent = None):
    super(Thumbnailer, self).__init__(parent)
    self.stopped = False
    self.completed = False
    self.running = False
    self.widget = ListWidget
  
  def initialize(self, queue):
    self.stopped = False
    self.completed = False
    self.running = True
  
  def stop(self):
    self.stopped = True
    self.running = False
    self.queue = []
  
  def run(self):
    if not self.running:
      self.process()
    
    self.stop()
  
  def process(self):
    if not os.path.exists('./djvu_backup/'):  os.mkdir('./djvu_backup/')
    if not os.path.exists('./djvu_backup/thumbnails/'):  os.mkdir('./djvu_backup/thumbnails/')
    
    for i in range(self.widget.count()):
      item = self.widget.item(i)
      
      if item.icon().isNull():
        djvu_backup = './djvu_backup/' + os.path.splitext(os.path.split(str(item.statusTip()))[1])[0]
        thumbnail = './djvu_backup/thumbnails/' + os.path.splitext(os.path.split(str(item.statusTip()))[1])[0]
        
        Image.open(str(item.statusTip())).save(djvu_backup, 'TIFF')
        
        thumb_image = Image.open(str(item.statusTip()))
        thumb_image.thumbnail([72, 72])
        thumb_image.save(thumbnail, 'TIFF')
        
        icon = QtGui.QImage(thumbnail)
        
        self.emit(QtCore.SIGNAL('makeIcon(int, QImage)'), i, icon)
    
    self.queue = []
