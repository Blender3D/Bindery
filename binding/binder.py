import os, time, shutil, glob, sys
import organizer, ocr, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from encoder import *

class Binder(QThread):
  def __init__(self, parent = None):
    super(Binder, self).__init__(parent)
  
  
  
  def initialize(self, pages, options, outfile):
    self.pages = pages
    self.options = options
    self.outFile = outfile
    
    self.book = organizer.Book()
    self.enc = Encoder(self.options)
    self.ocr = ocr.OCR(self.options)
    
    self.connect(self.enc, SIGNAL('updateProgress(int, int)'), self.updateProgress)
    self.connect(self.enc, SIGNAL('error(QString)'), self.error)
  
  
  
  def error(self, message):
    self.emit(SIGNAL('error(QString)'), message)
  
  
  def add_file(self, filename, type = 'page'):
    if type == 'page':
      self.book.insert_page(filename)
    else:
      self.book.suppliments[type] = filename

    return None
  
  
  
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
      boxing = self.ocr.analyze_image(page.path)
      page.text = self.ocr.translate(boxing)
      
      self.emit(SIGNAL('updateProgress(int, QString)'), 25 + int(25 * (1 - float(len(self.queue)) / float(self.total))), 'Performing OCR')
      self.emit(SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QColor(190, 255, 190, 120))
    return None
  
  
  def run(self):
    self.die = False
    
    if not self.die:
      for page in self.pages:
        if page.grayscale:
          utils.simple_exec('convert "{0}" -type Grayscale "{0}.grayscale"'.format(page.filepath))
          page.filepath += '.grayscale'
    
    for page in self.pages:
      self.add_file(page.filepath, 'page')
      print page.filepath
    
    if not self.die:
      self.analyze()
    
    if not self.die:
      self.book.get_dpi()
    
    if self.options['ocr'] and not self.die:
      self.get_ocr()
    
    if not self.die:
      self.enc.initialize(self.book, self.outFile)
      self.enc.start()
