from datetime import datetime
#import inspect

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DebugLog(QTreeWidget):
  def __init__(self, parent = None):
    super(DebugLog, self).__init__(parent)
  
  def log(self, message, level = 'normal'):
    time = datetime.now()
    timestamp = '{hour}:{minute}:{second}'.format(hour = str(time.hour).zfill(2), minute = str(time.minute).zfill(2), second = str(time.second).zfill(2))
    
    #self.addTopLevelItem(QTreeWidgetItem([timestamp, inspect.getouterframes(inspect.currentframe(), 2)[1][3], message, level]))
    self.addTopLevelItem(QTreeWidgetItem([timestamp, 'function', message, level]))
