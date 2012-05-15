try:
  from djvubind import encode
except:
  from ..djvubind import encode

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DjVuEncoder(QThread, encode.Encoder):
  def __init__(self, options, parent = None):
    super(QThread, self).__init__(parent)
    
    self.opts = options
    
    self.count = 0
    self.done = 0
  
  def progress(self):
    self.done += 1
    self.sendProgress(100.0 * float(self.done) / len(self.book.pages))

  def sendProgress(self, percent):
    self.emit(SIGNAL('updateProgress(int, int)'), (percent * 0.50) + 50.0, self.count)
    self.count += 1
  
  def sendError(self, message):
    self.emit(SIGNAL('error(QString)'), message)
    self.exit()
  
  def run(self):
    self.enc_book(self.book, self.opts['output_file'])
