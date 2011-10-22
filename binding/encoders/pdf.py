import os, time, shutil, glob, sys, shlex, platform
from subprocess import Popen, PIPE, STDOUT

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
  
  def _jbig2(self, basename, inputs):
    process = Popen(shlex.split('jbig2 -v -b "{0}" -p -s "{1}"'.format(basename, '" "'.join(inputs))), stdout = PIPE, stderr = STDOUT)

    count = 0

    while True:
      output = process.stdout.readline()

      if output == '' and process.poll() != None:
        break

      if output != '':
        count += 1
        
        if count % 2:
          self.progress()
          
          if count == 2 * len(inputs) - 1:
            break

    return None
    
  def _pdfpy(self, basename, output):
    pdf = utils.execute('pdf.py "{0}" > "{1}"'.format(basename, output))
    
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
    
    if self.opts['bitonal_encoder'] == 'jbig2':
      self._jbig2('jbig2', [page.path for page in book.pages])
      self._pdfpy('jbig2', self.outfile)
      
#      os.remove('jbig2.*')
    
    if self.opts['ocr']:
      for page in book.pages:
        handle = open('ocr.txt', 'w')
        handle.write(page.text)
        handle.close()
        
        page_number = book.pages.index(page) + 1
        utils.simple_exec('pdfsed -e "select {0}; remove-txt; set-txt \'ocr.txt\'; save" "{1}"'.format(page_number, outfile))
        os.remove('ocr.txt')

    self.exit()
    
    return None
