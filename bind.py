import os, time, shutil, glob, sys
import organizer, ocr, utils

from PyQt4 import QtCore, QtGui
from encoder import *

class Binder(QtCore.QThread):
  '''
  Class for binding the actual book
  '''
  
  def __init__(self, parent = None):
    super(Binder, self).__init__(parent)
  
  
  
  def initialize(self, pages, options, outfile):
    self.pages = pages
    self.options = options
    self.outFile = outfile
    
    self.book = organizer.Book()
    self.enc = Encoder(self.options)
    self.ocr = ocr.OCR(self.options)
    
    self.connect(self.enc, QtCore.SIGNAL('updateProgress(int, int)'), self.updateProgress)
  
  
  
  def add_file(self, filename, type = 'page'):
    """
    Adds a file to the project.
    type can be 'page', 'cover_front', 'cover_back', 'metadata', or 'bookmarks'.
    """

    # Hand the files over to self.book to manage.
    if type == 'page':
      self.book.insert_page(filename)
    else:
      self.book.suppliments[type] = filename

    return None
  
  
  
  def analyze(self):
    """
    Retrieve and store information about each image (dpi, bitonal, etc.).
    """

    # Create queue and populate with pages to process
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
      
      if self.options['ocr']:
        self.emit(QtCore.SIGNAL('updateProgress(int, QString)'), int(25 * (1 - float(len(self.queue)) / float(self.total))), 'Analyzing...')
      else:
        self.emit(QtCore.SIGNAL('updateProgress(int, QString)'), int(50 * (1 - float(len(self.queue)) / float(self.total))), 'Analyzing...')
      
      self.emit(QtCore.SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QtGui.QColor(210, 255, 210, 120))
      
    return None
  
  
  def updateProgress(self, percent, item):
    self.emit(QtCore.SIGNAL('updateProgress(int, QString)'), int(percent), 'Binding the book...')
    self.emit(QtCore.SIGNAL('updateBackground(int, QColor)'), int(item), QtGui.QColor(170, 255, 170, 120))
    
    if int(percent) == 100:
      time.sleep(0.5)
      self.emit(QtCore.SIGNAL('finishedBinding'))
  
  def get_ocr(self):
    """
    Performs optical character analysis on all images, excluding covers.
    """

    # Create queue and populate with pages to process
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
      
      self.emit(QtCore.SIGNAL('updateProgress(int, QString)'), 25 + int(25 * (1 - float(len(self.queue)) / float(self.total))), 'Performing OCR...')
      self.emit(QtCore.SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QtGui.QColor(190, 255, 190, 120))
    return None
  
  
  def run(self):
    self.die = False
    
    for page in self.pages:
      self.add_file(page, 'page')
    
    if not self.die:
      self.analyze()
    
    if not self.die:
      self.book.get_dpi()
    
    if self.options['ocr'] and not self.die:
      self.get_ocr()
    
    if not self.die:
      self.enc.initialize(self.book, self.outFile)
      self.enc.start()
