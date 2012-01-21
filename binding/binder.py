import os, time, shutil, glob, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .djvubind import ocr, utils

from . import organizer

from .encoders.djvu import DjVuEncoder
from .encoders.pdf import PDFEncoder

class Binder(QThread):
  def __init__(self, parent = None):
    super(Binder, self).__init__(parent)
  
  def initialize(self, pages, options):
    self.pages = pages
    self.options = options
    self.book = organizer.Book()
    
    if self.options['output_format'] == 'djvu':
      self.enc = DjVuEncoder(self.options)
    elif self.options['output_format'] == 'pdf':
      self.enc = PDFEncoder(self.options)
    
    self.ocr = ocr.engine(self.options['ocr_engine'], self.options['ocr_options'])
    
    self.connect(self.enc, SIGNAL('updateProgress(int, int)'), self.updateProgress)
    self.connect(self.enc, SIGNAL('error(QString)'), self.error)
  
  def error(self, message):
    self.emit(SIGNAL('error(QString)'), message)
  
  def add_file(self, filename, type = 'page'):
    if type == 'page':
      self.book.insert_page(filename)
    else:
      self.book.suppliments[type] = filename

    return self.book.pages[-1]
  
  def analyze(self):
    queue = []
    
    for page in self.book.pages:
      queue.append(page)
    
    self.queue = queue
    self.quit = False
    self.total = len(self.queue)
    
    while not self.quit:
      if len(self.queue) == 0:
        self.quit = True
        break
      
      page = self.queue.pop()
      page.is_bitonal()
      page.get_dpi()
      page.get_size()

      if page.make_grayscale and not page.bitonal:
        utils.simple_exec('convert "{0}" -type Grayscale "{0}.grayscale"'.format(page.path))
        page.path += '.grayscale'
      
      basePercent = 25 if self.options['ocr'] else 50
      
      self.emit(SIGNAL('updateProgress(int, QString)'), int(basePercent * (1 - float(len(self.queue)) / float(self.total))), 'Analyzing')
      self.emit(SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QColor(210, 255, 210, 120))
      
    return None
  
  def updateProgress(self, percent, item):
    self.emit(SIGNAL('updateProgress(int, QString)'), int(percent), 'Binding the book')
    self.emit(SIGNAL('updateBackground(int, QColor)'), int(item), QColor(170, 255, 170, 120))
    
    if int(percent) == 100:
      time.sleep(0.5)
      self.emit(SIGNAL('finishedBinding'))
  
  def get_ocr(self):
    queue = []
    
    for page in self.book.pages:
      queue.append(page)
    
    self.queue = queue
    self.total = len(self.queue)
    self.quit = False
    
    while not self.quit:
      if len(self.queue) == 0:
        self.quit = True
        break
      
      page = self.queue.pop()
      boxing = self.ocr.analyze(page.path)
      page.text = ocr.translate(boxing)
      
      self.emit(SIGNAL('updateProgress(int, QString)'), 25 + int(25 * (1 - float(len(self.queue)) / float(self.total))), 'Performing OCR')
      self.emit(SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QColor(190, 255, 190, 120))
    
    return None
  
  def run(self):
    self.die = False
    
    for page in self.pages:
      book_page = self.add_file(page.filepath, 'page')
      book_page.make_grayscale = page.grayscale
      print(page.filepath)
    
    if not self.die:
      self.analyze()
    
    if not self.die:
      self.book.get_dpi()
    
    if self.options['ocr'] and not self.die:
      self.get_ocr()
    
    if not self.die:
      self.enc.book = self.book
      self.enc.start()
