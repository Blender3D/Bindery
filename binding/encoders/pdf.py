import os, time, shutil, glob, sys, shlex, platform, struct
from subprocess import Popen, PIPE, STDOUT

from itertools import count

from binding import organizer, ocr, utils

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dict:
  def __init__(self, values = {}):
    self.values = values
  
  def __str__(self):
    temp = '<<\n'
    
    for key, value in self.values.items()[::-1]:
      temp += '/{key} {value}\n'.format(key=key, value=value)
    
    return temp + '>>\n'

class Obj:
  ids = count(1)
  
  def __init__(self, d = {}, stream = None):
    if stream is not None:
      d['Length'] = str(len(stream))
    
    self.dictionary = Dict(d)
    self.stream = stream
    self.id = self.ids.next()
  
  def addTo(self, document):
    document.add_object(self)
    
    return self
  
  def ref(self):
    return '{id} 0 R'.format(id=self.id)
  
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
    string = ['%PDF-1.5']
    size = 9
    offsets = []

    for object in self.objects:
      offsets.append(size)
      
      obj_size = '{id} 0 obj'.format(id=object.id)
      str_object = str(object)
      
      string.append(obj_size)
      string.append(str_object)
      
      size += len(obj_size) + len(str_object) + 2
    
    string.append('xref')
    string.append('0 {size}'.format(size=len(offsets) + 1))
    string.append('0000000000 65535 f ')
    
    for offset in offsets:
      string.append('%010d 00000 n ' % offset)
    
    string.append('')
    string.append('trailer')
    string.append('<< /Size {size}\n/Root 1 0 R\n/Info 2 0 R>>'.format(size=len(offsets) + 1))
    string.append('startxref')
    string.append(str(size))
    string.append('%%EOF')

    return '\n'.join(string)


def loadImage(image, oc, procSet):
  if '/ImageC' not in procSet:
    procSet.append('/ImageC')

  image_obj = Obj({
    'Type':             '/XObject',
    'Subtype':          '/Image',
    'OC':               oc.ref(),
    'Width':            image.width,
    'Height':           image.height,
    'Interpolate':      'True',
    'Filter':           '/JPXDecode',
    'BitsPerComponent': '24',
    'ColorSpace':       '/DeviceRGB'
  }, open(image.path, 'rb').read())

  return image_obj


class PDFEncoder(QThread):
  def __init__(self, options, parent = None):
    super(PDFEncoder, self).__init__(parent)
    
    self.count = 0
    self.done = 0
    
    self.options = options
  
  def progress(self):
    self.done += 1
    self.sendProgress(100.0 * float(self.done) / float(self.total))

  def sendProgress(self, percent):
    self.emit(SIGNAL('updateProgress(int, int)'), (percent * 0.50) + 50.0, self.count)
    self.count += 1
  
  def sendError(self, message):
    self.emit(SIGNAL('error(QString)'), message)
    self.exit()
  
  def run(self):
    self.enc_book(self.book, self.options['output_file'])
  
  def _jbig2pdf(self, symboltable, book):
    document = Document()
    
    metadata = Obj({
      'Creator':      '(Bindery)',
      'Producer':     '(Bindery)',
      'CreationDate': '(D:{date}--5\'00)'.format(date=time.strftime('%Y%m%d%H%M%S', time.gmtime()))
    })
    
    for option in ['title', 'author', 'subject']:
      if self.options[option]:
        metadata.dictionary[option.title()] = '({value})'.format(value=self.options[option])
    
    document.add_object(metadata)
    
    outlines = Obj({
      'Type': '/Outlines',
      'Count': '0'
    }).addTo(document)
    
    pages = Obj({
      'Type' : '/Pages'
    }).addTo(document)
    
    creator = Obj({
      'Subtype': '/Artwork',
      'Creator': '(Bindery)',
      'Feature': '/Layers'
    }).addTo(document)
    
    foreground = Obj({
      'Type':    '/OGC',
      'Name':    '(Foreground)',
      'Usage':   '<</CreatorInfo {ref} >>'.format(ref=creator.ref()),
      'Intent' : '[/View/Design]'
    }).addTo(document)
    
    background = Obj({
      'Type':    '/OGC',
      'Name':    '(Background)',
      'Usage':   '<</CreatorInfo {ref} >>'.format(ref=creator.ref()),
      'Intent' : '[/View/Design]'
    }).addTo(document)
    
    catalog = Obj({
      'Type':         '/Catalog',
      'Outlines':     outlines.ref(),
      'Pages':        pages.ref(),
      'PageLayout':   '/TwoPageRight',
      'OCProperties': '<< /OCGs[{fore} {back}] /D<< /Intent /View /BaseState (ON) /Order[{fore} {back}] >>>>'.format(
        fore=foreground.ref(),
        back=background.ref())
    }).addTo(document)

    symd = Obj({}, open(symboltable, 'rb').read()).addTo(document)
    page_objects = []

    for page in book.pages:
      images = 0
      procSet = ['/PDF', '/ImageB']
      
      if page.graphical:
        graphical = Obj({
          'Type':             '/XObject',
          'Subtype':          '/Image',
          'Width':            str(page.width),
          'Height':           str(page.height),
          'ColorSpace':       '/DeviceRGB',
          'Interpolate':      'true',
          'Filter':           '/JPXDecode',
          'BitsPerComponent': '24',
          'OC':                background.ref()
        }, open(page.graphical, 'rb').read()).addTo(document)
        
        if '/ImageC' not in procSet:
          procSet.append('/ImageC')
        
        if page.textual:
          textual = Obj({
            'Type':             '/XObject',
            'Subtype':          '/Image',
            'Width':            str(page.width),
            'Height':           str(page.height),
            'ColorSpace':       '/DeviceGray',
            'BitsPerComponent': '1',
            'Filter':           '/JBIG2Decode',
            'DecodeParms':      ' << /JBIG2Globals {ref} >>'.format(ref=symd.ref())
          }, open(page.textual, 'rb').read()).addTo(document)
        
        contents = Obj({
          'Filter': '/FlateDecode'
        })
        resobj = Obj({})
        resources = Obj({
          'XObject': resobj.ref()
        })
        
        foreground.dictionary['SMask'] = textual.ref()
        
        page = Obj({
          'Type':     '/Page',
          'Parent':   outlines.ref(),
          'MediaBox': '[ 0 0 {width} {height} ]'.format(
            width=float(page.width * 72) / book.dpi,
            height=float(page.height * 72) / book.dpi),
          'Contents':  group.ref(),
          'Resources': procset.ref()
        }).addTo(document)
        
      else:
        xobj = Obj({
          'Type':              '/XObject',
          'Subtype':           '/Image',
          'OC':                ocref,
          'Width':             str(page.width),
          'Height':            str(page.height),
          'ImageMask':         'true',
          'ColorSpace':        '/DeviceGray',
          'BitsPerComponent':  '1',
          'Filter':            '/JBIG2Decode',
          'DecodeParms':       "<< /JBIG2Globals {ref} >>".format(ref=symd.ref())
        }, open(jbig2, 'rb').read())
        
        contents = Obj({}, 'q {width} 0 0 {height} 0 0 cm /Im1 Do Q'.format(
          width=float(page.width * 72) / book.dpi,
          height=float(page.height * 72) / book.dpi)
        ).addTo(document)
        
        resources = Obj({
          'ProcSet': '[/PDF /ImageB]',
          'XObject': '<< /Im1 {ref} >>'.format(ref=xobj.ref)
        }).addTo(document)
        
        page = Obj({
          'Type':     '/Page',
          'Parent':   outlines.ref(),
          'MediaBox': '[ 0 0 {width} {height} ]'.format(
            width=float(page.width * 72) / book.dpi,
            height=float(page.height * 72) / book.dpi),
          'Contents':  contents.ref(),
          'Resources': resources.ref()
        }).addTo(document)
        
      page_objects.append(page)
    
    pages.dictionary.values['Count'] = str(len(page_objects))
    pages.dictionary.values['Kids'] = '[' + ' '.join([x.ref() for x in page_objects]) + ']'
    
    output = open(self.options['output_file'], 'wb')
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

  def enc_book(self, book, outfile):
    Obj.ids = count(1)
    
    self.total = len(book.pages)
    self.done = 0
    
    if self.options['bitonal_encoder'] == 'jbig2':
      bitonals = 0
      
      for page in book.pages:
        basename = os.path.splitext(os.path.split(page.path)[-1])[0]
        folder = os.path.split(page.path)[0]

        if page.bitonal:
          page.textual = os.path.abspath('jbig2.{number}'.format(number = str(bitonals).zfill(4)))
        else:
          utils.execute('convert -opaque black "{input}" "{basename}.graphics.tif"'.format(input = page.path, basename = basename))
          utils.execute('convert +opaque black "{input}" "{basename}.text.tif"'.format(input = page.path, basename = basename))
          #utils.execute('convert "{basename}.graphics.tif"  -limit memory 64 -limit map 128 -define jp2:mode=real -define jp2:rate=0.015625 -define jp2:numrlvls=4 "{basename}.graphics.jp2"'.format(basename = basename))
          
          page.textual = os.path.abspath('jbig2.{number}'.format(number = str(bitonals).zfill(4)))
          page.graphical = os.path.abspath(basename + '.graphics.jp2')
          
          bitonals += 1
          
      self._jbig2('jbig2', [page.textual for page in book.pages if page.textual])
      self._jbig2pdf('jbig2.sym', book)
    
    if self.options['ocr']:
      for page in book.pages:
        handle = open('ocr.txt', 'w')
        handle.write(page.text)
        handle.close()
        
        page_number = book.pages.index(page) + 1
        utils.simple_exec('pdfsed -e "select {0}; remove-txt; set-txt \'ocr.txt\'; save" "{1}"'.format(page_number, outfile))
        os.remove('ocr.txt')
    
    self.exit()
    
    return None
