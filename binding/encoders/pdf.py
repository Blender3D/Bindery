import os, time, shutil, glob, sys, platform
from pyPdf import PdfFileWriter, PdfFileReader

from binding import organizer, ocr, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PDFEncoder(QThread):
  def __init__(self, opts, parent = None):
    super(PDFEncoder, self).__init__(parent)
    
    self.opts = opts
    
    self.count = 0
    self.done = 0
    
    self.book = None
    self.outfile = None
    
    self.dep_check()
  
  def progress(self):
    self.done += 1
    self.sendProgress(100.0 * float(self.done) / float(self.total))

  def sendProgress(self, percent):
    self.emit(SIGNAL('updateProgress(int, int)'), (percent * 0.50) + 50.0, self.count)
    self.count += 1
  
  def sendError(self, message):
    self.emit(SIGNAL('error(QString)'), message)
    self.exit()
  
  def initialize(self, book, outfile):
    self.book = book
    self.outfile = outfile
    self.pages = len(self.book.pages)
  
  def run(self):
    self.enc_book(self.book, self.outfile)
  
  def _c44(self, infile, outfile, dpi):
    if os.path.splitext(infile) not in ['.pgm', '.ppm', '.jpg', '.jpeg']:
      utils.execute('convert {0} {1}'.format(infile, 'temp.ppm'))
      infile = 'temp.ppm'
    
    utils.execute('c44 -dpi {0} {1} "{2}" "{3}"'.format(dpi, self.opts['c44_options'], infile, outfile))

    if not os.path.isfile(outfile):
      self.sendError('encode.Encoder._c44(): No encode errors, but "{0}" does not exist!'.format(outfile))

    if infile == 'temp.ppm' and os.path.isfile('temp.ppm'):
      os.remove('temp.ppm')

    return None

  def _cjb2(self, infile, outfile, dpi):
    utils.execute('cjb2 -dpi {0} {1} "{2}" "{3}"'.format(dpi, self.opts['cjb2_options'], infile, outfile))
    
    if not os.path.isfile(outfile):
      self.sendError('encode.Encoder._cpalpdf(): No encode errors, but "{0}" does not exist!'.format(outfile))
    
    return None

  def dep_check(self):
    if not utils.is_executable(self.opts['bitonal_encoder']):
      self.sendError('encoder "{0}" is not installed.'.format(self.opts['bitonal_encoder']))
    if not utils.is_executable(self.opts['color_encoder']):
      self.sendError('encoder "{0}" is not installed.'.format(self.opts['color_encoder']))
    
    return None

  def pdf_insert(self, infile, pdffile, page_num = None):
    output = PdfFileWriter()
    
    print infile, pdffile
    
    if not os.path.isfile(pdffile):
      shutil.copy(infile, pdffile)
    else:
      input = PdfFileReader(file(infile, 'rb'))
      
      if page_num is None:
        for page in input.pages.getNumPages():
          output.addPage(page)
      else:
        for i in range(input.pages.getNumPages()):
          page = input.getPage(i)
          output.insertPage(page, page_num + i)
      
      stream = file(pdffile, 'wb')
      output.write(stream)
      stream.close()

  def enc_book(self, book, outfile):
    self.total = len(book.pages)
    self.done = 0
    
    tempfile = 'temp.pdf'
    
    if self.opts['bitonal_encoder'] == 'cjb2':
      for page in book.pages:
        if page.bitonal:
          self._cjb2(page.path, tempfile, page.dpi)
          self.pdf_insert(tempfile, outfile)
          os.remove(tempfile)
          
          self.progress()
    
    if self.opts['color_encoder'] == 'c44':
      for page in book.pages:
        if not page.bitonal:
          page_number = book.pages.index(page) + 1
          self._c44(page.path, tempfile, page.dpi)
          self.pdf_insert(tempfile, outfile, page_number)
          os.remove(tempfile)
          
          self.progress()
    
    if self.opts['ocr']:
      for page in book.pages:
        handle = open('ocr.txt', 'w')
        handle.write(page.text)
        handle.close()
        
        page_number = book.pages.index(page) + 1
        utils.simple_exec('pdfsed -e "select {0}; remove-txt; set-txt \'ocr.txt\'; save" "{1}"'.format(page_number, outfile))
        os.remove('ocr.txt')

    if os.path.isfile(tempfile):
      os.remove(tempfile)
    
    self.exit()
    
    return None
