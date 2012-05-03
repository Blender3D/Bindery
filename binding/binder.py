import os, time, shutil, glob, sys, tempfile

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import djvubind.ocr

from . import organizer, ocr

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

    if self.options['ocr']:
      if self.options['ocr_engine'] == 'tesseract':
        self.ocr = djvubind.ocr.Tesseract(self.options)
      elif self.options['ocr_engine'] == 'cuneiform':
        self.ocr = djvubind.ocr.Cuneiform(self.options)
    else:
      self.ocr = False
    
    self.connect(self.enc, SIGNAL('updateProgress(int, int)'), self.updateProgress)
    self.connect(self.enc, SIGNAL('error(QString)'), self.error)
  
  def error(self, message):
    self.emit(SIGNAL('error(QString)'), message)
    self.terminate()
  
  def add_file(self, filename, category='page'):
    if category == 'page':
      self.book.insert_page(filename)
    else:
      self.book.suppliments[category] = filename

    return self.book.pages[-1]
  
  def analyze(self):
    self.queue = self.book.pages[:]
    self.quit = False
    self.total = len(self.queue)
    base_percent = 25 + 25 * (not self.options['ocr'])
    
    while not self.quit:
      if len(self.queue) == 0:
        self.quit = True
        break

      self.emit(
        SIGNAL('updateProgress(int, QString)'),
        int(base_percent * (1 - float(len(self.queue)) / float(self.total))),
        'Analyzing ({number}/{total})'.format(
          number=len(self.book.pages) - len(self.queue) + 1,
          total=len(self.book.pages)
        )
      )
      
      page = self.queue.pop()
      page.is_bitonal()
      page.get_dpi()
      page.get_size()
      
      if page.grayscale and not page.bitonal:
        utils.simple_exec('convert "{0}" -type Grayscale "{0}.grayscale"'.format(page.path))
        page.path += '.grayscale'
      
      self.emit(SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QColor(210, 255, 210, 120))
      
    return None
  
  def updateProgress(self, percent, item):
    self.emit(SIGNAL('updateProgress(int, QString)'), int(percent), 'Binding the book')
    self.emit(SIGNAL('updateBackground(int, QColor)'), int(item), QColor(170, 255, 170, 120))
    
    if int(percent) == 100:
      os.remove(self.metadata.name)
      
      time.sleep(0.5)
      self.emit(SIGNAL('finishedBinding'))
  
  def get_ocr(self):
    self.queue = self.book.pages[:]
    self.total = len(self.queue)
    self.quit = False
    
    while not self.quit:
      if len(self.queue) == 0:
        self.quit = True
        break
      
      self.emit(
        SIGNAL('updateProgress(int, QString)'),
        25 + int(25 * (1 - float(len(self.queue)) / float(self.total))),
        'Performing OCR ({number}/{total})'.format(
          number=len(self.book.pages) - len(self.queue) + 1,
          total=len(self.book.pages)
        )
      )
      
      page = self.queue.pop()
      
      if self.options['ocr']:
        page.text = djvubind.ocr.translate(self.ocr.analyze(page.path))
      
      self.emit(SIGNAL('updateBackground(int, QColor)'), len(self.book.pages) - len(self.queue) - 1, QColor(190, 255, 190, 120))
    
    return None
  
  def run(self):
    self.die = False
    self.book.pages = self.pages[:]
    
    if os.path.isfile(self.options['output_file']):
      os.remove(self.options['output_file'])
    
    if not self.die:
      self.analyze()
    
    if not self.die:
      self.book.get_dpi()
    
    self.metadata = tempfile.NamedTemporaryFile(delete=False)
    
    for prop in ['Title', 'Author', 'Subject', 'Keywords']:
      self.metadata.write('{prop}{sep} "{value}"\n'.format(
        prop=prop,
        sep=':' if self.options['output_format'] == 'pdf' else '',
        value=self.options[prop.lower()].replace('\\', '\\\\').replace('"', '\\"')
      ).encode())
    
    self.metadata.close()
    
    self.book.suppliments['metadata'] = self.metadata.name
  
    if self.options['ocr'] and not self.die:
      self.get_ocr()
      self.emit(SIGNAL('ocrFinished'))
    
    if not self.die:
      self.enc.book = self.book
      self.enc.start()
