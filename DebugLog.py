from PyQt4 import QtCore, QtGui

class DebugLog(QtGui.QTextEdit):
  def __init__(self, parent = None):
    super(DebugLog, self).__init__(parent)
  
  
  
  def add(self, message, status = 'normal'):
    if self.toPlainText() != '':
      self.setText(self.toPlainText() + '\n' + message)
    else:
      self.setText(message)
