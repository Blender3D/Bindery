import os, time, shutil, glob, sys, shlex, platform, struct
from subprocess import Popen, PIPE, STDOUT

from binding import organizer, ocr, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dict:
  def __init__(self, values = {}):
    self.values = values
  
  def __str__(self):
    temp = '<< '
    
    for (key, value) in self.values.items():
      temp += '/{key} {value}\n'.format(key = key, value = value)
    
    return temp + '>>\n'

global_next_id = 1

class Obj:
  next_id = 1
  
  def __init__(self, d = {}, stream = None):
    global global_next_id

    if stream is not None:
      d['Length'] = str(len(stream))
    
    self.dictionary = Dict(d)
    self.stream = stream
    self.id = global_next_id
    global_next_id += 1

  def __str__(self):
    stream = str(self.dictionary)
    
    if self.stream is not None:
      stream += 'stream\n' + self.stream + '\nendstream\n'
    
    return stream + 'endobj\n'

class Document:
  def __init__(self):
    self.objects = []
    self.pages = []

  def add_object(self, object):
    self.objects.append(object)
    
    return object

  def add_page(self, object):
    self.pages.append(object)
    
    return self.add_object(object)

  def __str__(self):
    string = ['%PDF-1.4']
    size = 9
    offsets = []

    for object in self.objects:
      offsets.append(size)
      
      obj_size = '{id} 0 obj'.format(id = object.id)
      str_object = str(object)
      
      string.append(obj_size)
      string.append(str_object)
      
      size += len(obj_size) + len(str_object) + 2
    
    string.append('xreference')
    string.append('0 {size}'.format(size = len(offsets) + 1))
    string.append('0000000000 65535 f ')
    
    for offset in offsets:
      string.append('%010d 00000 n ' % offset)
    
    string.append('')
    string.append('trailer')
    string.append('<< /Size {size}\n/Root 1 0 R >>'.format(size = len(offsets) + 1))
    string.append('startxreference')
    string.append(str(size))
    string.append('%%EOF')

    return '\n'.join(string)

def reference(x):
  return '%d 0 R' % x



class PDFEncoder(QThread):
  def __init__(self, opts, parent = None):
    super(PDFEncoder, self).__init__(parent)
    
    self.opts = opts
    
    self.count = 0
    self.done = 0
    
    self.book = None
    self.outfile = None
  
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
  
  def _jbig2pdf(self, symboltable = 'jbig2.sym', pagefiles = glob.glob('jbig2.[0-9]*'), dpi = 600):
    document = Document()
    
    document.add_object(Obj({'Type':     '/Catalog',
                              'Outlines': reference(2),
                              'Pages':    reference(3)}))
    
    document.add_object(Obj({'Type': '/Outlines',
                             'Count': '0'}))
    
    pages = Obj({'Type' : '/Pages'})
    document.add_object(pages)
    
    symd = document.add_object(Obj({}, open(symboltable, 'rb').read()))
    page_objects = []

    pagefiles.sort()
    
    for page in pagefiles:
      contents = open(page, 'rb').read()
      width, height = struct.unpack('>II', contents[11:19])
      
      xobj = Obj({'Type':            '/XObject',
                  'Subtype':         '/Image',
                  'Width':            str(width),
                  'Height':           str(height),
                  'ColorSpace':       '/DeviceGray',
                  'BitsPerComponent': '1',
                  'Filter':           '/JBIG2Decode',
                  'DecodeParms':      ' << /JBIG2Globals {id} 0 R >>'.format(id = symd.id)},
                 contents)
      
      contents = Obj({}, 'q {width} 0 0 {height} 0 0 cm /Im1 Do Q'.format(width = float(width * 72) / dpi, height = float(height * 72) / dpi))
      resources = Obj({'ProcSet': '[/PDF /ImageB]',
                       'XObject': '<< /Im1 {id} 0 R >>'.format(id = xobj.id)})
      
      page = Obj({'Type':     '/Page',
                  'Parent':   '3 0 R',
                  'MediaBox': '[ 0 0 {width} {height} ]'.format(width = float(width * 72) / dpi, height = float(height * 72) / dpi),
                  'Contents':  reference(contents.id),
                  'Resources': reference(resources.id)})
      
      for object in [xobj, contents, resources, page]:
        document.add_object(object)
      
      page_objects.append(page)

      pages.dictionary.values['Count'] = str(len(page_objects))
      pages.dictionary.values['Kids'] = '[' + ' '.join([reference(x.id) for x in page_objects]) + ']'
    
    output = open(self.outfile, 'wb')
    output.write(str(document))
    output.close()

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
    
  def pdf_insert(self, infile, pdffile, page_num = None):
    output = PdfFileWriter()
    
    print infile, pdffile
    
    if not os.path.isopen(pdffile):
      shutil.copy(infile, pdffile)
    else:
      input = PdfFileReader(open(infile, 'rb'))
      
      if page_num is None:
        for page in input.pages.getNumPages():
          output.addPage(page)
      else:
        for i in range(input.pages.getNumPages()):
          page = input.getPage(i)
          output.insertPage(page, page_num + i)
      
      stream = open(pdffile, 'wb')
      output.write(stream)
      stream.close()

  def enc_book(self, book, outfile):
    self.total = len(book.pages)
    self.done = 0
    
    if self.opts['bitonal_encoder'] == 'jbig2':
      self._jbig2('jbig2', [page.path for page in book.pages])
      self._jbig2pdf('jbig2.sym', glob.glob('jbig2.[0-9]*'), book.dpi)
    
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
