import os, time, shutil, glob, sys, platform

from binding import organizer, ocr, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DjVuEncoder(QThread):
  def __init__(self, opts, parent = None):
    super(DjVuEncoder, self).__init__(parent)
    
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
      self.sendError('encode.Encoder._cpaldjvu(): No encode errors, but "{0}" does not exist!'.format(outfile))
    
    return None

  def _cpaldjvu(self, infile, outfile, dpi):
    if os.path.splitext(infile) not in ['.ppm']:
      utils.execute('convert {0} {1}'.format(infile, 'temp.ppm'))
      infile = 'temp.ppm'
    
    utils.execute('cpaldjvu -dpi {0} {1} "{2}" "{3}"'.format(dpi, self.opts['cpaldjvu_options'], infile, outfile))
    
    if not os.path.isfile(outfile):
      self.sendError('encode.Encoder._cpaldjvu(): No encode errors, but "{0}" does not exist!'.format(outfile))
    
    if infile == 'temp.ppm' and os.path.isfile('temp.ppm'):
      os.remove('temp.ppm')
    
    return None

  def _csepdjvu(self, infile, outfile, dpi):
    utils.execute('convert -opaque black "{0}" "temp_graphics.tif"'.format(infile))
    utils.execute('convert +opaque black "{0}" "temp_textual.tif"'.format(infile))

    self._cjb2('temp_textual.tif', 'enc_bitonal_out.djvu', dpi)
    
    if platform.system() == 'Windows':
      utils.execute('ddjvu -format=rle "enc_bitonal_out.djvu" "temp_textual.rle"')
    else:
      utils.execute('ddjvu -format=rle -v "enc_bitonal_out.djvu" "temp_textual.rle"')
    
    utils.execute('convert temp_graphics.tif temp_graphics.ppm')
    
    with open('temp_merge.mix', 'wb') as mix:
      with open('temp_textual.rle', 'rb') as rle:
        buffer = rle.read(1024)
        
        while buffer:
          mix.write(buffer)
          buffer = rle.read(1024)
      
      with open('temp_graphics.ppm', 'rb') as ppm:
        buffer = ppm.read(1024)
        
        while buffer:
          mix.write(buffer)
          buffer = ppm.read(1024)
    
    utils.execute('csepdjvu -d {0} {1} "temp_merge.mix" "temp_final.djvu"'.format(dpi, self.opts['csepdjvu_options']))

    if not os.path.isfile(outfile):
      shutil.move('temp_final.djvu', outfile)
    else:
      utils.execute('djvm -i {0} "temp_final.djvu"'.format(outfile))
    
    for tempfile in glob.glob('temp_*'):
      os.remove(tempfile)
    
    os.remove('enc_bitonal_out.djvu')
    
    return None

  def _minidjvu(self, infiles, outfile, dpi):
    tempfile = 'enc_temp.djvu'
    
    for cmd in utils.split_cmd('minidjvu -d {0} {1}'.format(dpi, self.opts['minidjvu_options']), infiles, tempfile):
      utils.execute(cmd)
      self.djvu_insert(tempfile, outfile)
    
    os.remove(tempfile)
    
    return None

  def dep_check(self):
    if not utils.is_executable(self.opts['bitonal_encoder']):
      self.sendError('encoder "{0}" is not installed.'.format(self.opts['bitonal_encoder']))
    if not utils.is_executable(self.opts['color_encoder']):
      self.sendError('encoder "{0}" is not installed.'.format(self.opts['color_encoder']))
    
    return None

  def djvu_insert(self, infile, djvufile, page_num = None):
    if not os.path.isfile(djvufile):
      shutil.copy(infile, djvufile)
    elif page_num is None:
      utils.execute('djvm -i "{0}" "{1}"'.format(djvufile, infile))
    else:
      utils.execute('djvm -i "{0}" "{1}" {2}'.format(djvufile, infile, int(page_num)))
  
  def enc_book(self, book, outfile):
    self.total = len(book.pages)
    self.done = 0
    
    tempfile = 'temp.djvu'
    
    if self.opts['bitonal_encoder'] == 'minidjvu':
      bitonals = []
      
      for page in book.pages:
        if page.bitonal:
          filepath = os.path.split(page.path)[1]
          bitonals.append(filepath)
      
      if len(bitonals) > 0:
        self._minidjvu(bitonals, tempfile, book.dpi)
        self.djvu_insert(tempfile, outfile)
        os.remove(tempfile)
        
        self.progress()
    elif self.opts['bitonal_encoder'] == 'cjb2':
      for page in book.pages:
        if page.bitonal:
          self._cjb2(page.path, tempfile, page.dpi)
          self.djvu_insert(tempfile, outfile)
          os.remove(tempfile)
          
          self.progress()
    
    if self.opts['color_encoder'] == 'csepdjvu':
      for page in book.pages:
        if not page.bitonal:
          page_number = book.pages.index(page) + 1
          self._csepdjvu(page.path, tempfile, page.dpi)
          self.djvu_insert(tempfile, outfile, page_number)
          os.remove(tempfile)
          
          self.progress()
    elif self.opts['color_encoder'] == 'c44':
      for page in book.pages:
        if not page.bitonal:
          page_number = book.pages.index(page) + 1
          self._c44(page.path, tempfile, page.dpi)
          self.djvu_insert(tempfile, outfile, page_number)
          os.remove(tempfile)
          
          self.progress()
    elif self.opts['color_encoder'] == 'cpaldjvu':
      for page in book.pages:
        if not page.bitonal:
          page_number = book.pages.index(page) + 1
          self._cpaldjvu(page.path, tempfile, page.dpi)
          self.djvu_insert(tempfile, outfile, page_number)
          os.remove(tempfile)
          
          self.progress()

    if self.opts['ocr']:
      for page in book.pages:
        handle = open('ocr.txt', 'w')
        handle.write(page.text)
        handle.close()
        
        page_number = book.pages.index(page) + 1
        utils.simple_exec('djvused -e "select {0}; remove-txt; set-txt \'ocr.txt\'; save" "{1}"'.format(page_number, outfile))
        os.remove('ocr.txt')

    if book.suppliments['cover_front']:
      dpi = int(utils.execute('identify -ping -format %x "{0}"'.format(book.suppliments['cover_front']), capture = True).decode('ascii').split(' ')[0])
      self._c44(book.suppliments['cover_front'], tempfile, dpi)
      self.djvu_insert(tempfile, outfile, 1)
      utils.execute('djvused -e "select 1; set-page-title cover; save" "{0}"'.format(outfile))
    
    if book.suppliments['cover_back']:
      dpi = int(utils.execute('identify -ping -format %x "{0}"'.format(book.suppliments['cover_back']), capture = True).decode('ascii').split(' ')[0])
      self._c44(book.suppliments['cover_back'], tempfile, dpi)
      self.djvu_insert(tempfile, outfile, -1)
    
    if book.suppliments['metadata']:
      utils.simple_exec('djvused -e "set-meta {0}; save" "{1}"'.format(book.suppliments['metadata'], outfile))
    
    if book.suppliments['bookmarks']:
      utils.simple_exec('djvused -e "set-outline {0}; save" "{1}"'.format(book.suppliments['bookmarks'], outfile))

    if os.path.isfile(tempfile):
      os.remove(tempfile)
    
    self.exit()
    
    return None
