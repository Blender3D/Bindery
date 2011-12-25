from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Previewer(QThread):
  def __init__(self, parent = None):
    super(Previewer, self).__init__(parent)
    
    self.image = None
    self.size = [None, None]

  def run(self):
    self.emit(SIGNAL('previewPage(QImage)'), QImage(self.image).scaled(self.size[0] * 4, self.size[1] * 4, aspectRatioMode = Qt.KeepAspectRatio).scaled(self.size[0], self.size[1], aspectRatioMode = Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation))
