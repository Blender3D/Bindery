import linecache, traceback

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Error(QMainWindow):
  def handleError(self, etype, value, trace):
    exception = ['<b>Traceback (most recent call last):</b>']
    
    while trace is not None:
      f = trace.tb_frame
      lineno = trace.tb_lineno
      co = f.f_code
      filename = co.co_filename
      name = co.co_name
      exception += ['  File "%s", line %d, in %s' % (filename, lineno, name)]
      
      linecache.checkcache(filename)
      line = linecache.getline(filename, lineno, f.f_globals)
      
      if line:
        exception += ['    ' + line.strip()]
      
      trace = trace.tb_next
    
    exception += traceback.format_exception_only(etype, value)
    
    self.ui.debugLog.setHtml(self.ui.debugLog.toHtml() + '<pre>' + '<br />'.join(exception) + '</pre>')
