import os, time, shutil, glob, sys, shlex, platform, struct
from subprocess import Popen, PIPE, STDOUT

try:
  from djvubind import organizer, utils
except:
  from ..djvubind import organizer, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PDFEncoder(QThread):
  def __init__(self, options, parent = None):
    super(PDFEncoder, self).__init__(parent)
    
    self.done = 0
    self.total = 0
    
    self.options = options
  
  def progress(self, amount=1):
    self.done += amount
    self.sendProgress(100.0 * float(self.done) / float(self.total))

  def sendProgress(self, percent):
    self.emit(SIGNAL('updateProgress(int, int)'), (percent * 0.50) + 50.0, int(self.done - 1))
  
  def sendError(self, message):
    self.emit(SIGNAL('error(QString)'), message)
    self.exit()
  
  def run(self):
    self.enc_book(self.book, self.options['output_file'])
  
  def _pdfbeads(self, command):
    process = Popen(shlex.split(command), stdout=PIPE, stderr=STDOUT)
    
    count = 0
    
    while True:
      output = process.stdout.readline().decode()

      if output == '' and process.poll() != None:
        break

      if output != '':
        if output.strip().startswith('Prepared data for'):
          self.progress(0.5)
        
        if output.strip().startswith('Processed'):
          self.progress(0.5)
        
    return None
  
  def enc_book(self, book, outfile):
    command = "pdfbeads "
    
    for option, parameter in [
      ('page_layout', '-P'),
      ('foreground_encoder', '-m'),
      ('background_encoder', '-b'),
      ('pages_per_dict', '-p'),
      ('binarization_threshold', '-t'),
      ('max_indexed_colors', '-x'),
    ]:
      command += ' {parameter} "{value}"'.format(
        parameter=parameter,
        value=self.options[option]
      )
    
    command += ' -o "{}"'.format(outfile.replace(' ', '\\ '))
    command += ' -M "{}"'.format(book.suppliments['metadata'])
    
    for page in book.pages:
      if ' ' in page.path:
        self.sendError('pdfbeads breaks when image paths have a space in them. Please rename the images and paths so that there are no spaces.')
        break
      command += ' "{}"'.format(page.path)
    
    self.total = len(book.pages)
    self._pdfbeads(command)
    
    for page in book.pages:
      filepath, filename = os.path.split(page.path)
      basename, extension = os.path.splitext(filename)
      
      jbig2 = os.path.join(filepath, basename + '.jbig2')
      symfile = os.path.join(filepath, basename + '.sym')
      
      for path in [jbig2, symfile]:
        if os.path.exists(path):
          os.remove(path)
    
    self.exit()
    
    return None
