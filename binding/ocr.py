import os, sys, re, shutil, difflib
import codecs
import HTMLParser
import utils

class hocrParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.boxing = []
    self.version = '0.8.0'
    self.data = ''

  def parse(self, data):
    self.data = data
    
    if "class='ocr_cinfo'" in self.data:
      self.version = '1.0.0'
    
    self.feed(data)
    
    return None

  def handle_starttag(self, tag, attrs):
    if self.version == '0.8.0':
      if (tag == 'br') or (tag == 'p'):
        if (len(self.boxing) > 0):
          self.boxing.append('newline')
      elif (tag == 'span'):
        element = {}
        element['start'] = self.data.find(self.get_starttag_text())
        element['end'] = self.data.find('>', element['start'])
        element['end'] = self.data.find('>', element['end']+1)
        element['end'] = element['end'] + 1
        element['text'] = self.data[element['start']:element['end']]
        
        pos = element['text'].find('>') + 1
        
        element['char'] = element['text'][pos:pos + 1]

        attrs = dict(attrs)['title']
        attrs = attrs.split()[1:]
        
        positions = {'xmin': int(attrs[0]),
                     'ymin': int(attrs[1]),
                     'xmax': int(attrs[2]),
                     'ymax': int(attrs[3])}
        
        positions['char'] = element['char']

        subst = {'"': '\\"',
                 "'": "\\'",
                 '\\': '\\\\'}
        
        if positions['char'] in subst.keys():
          positions['char'] = subst[positions['char']]
        
        self.boxing.append(positions)

        if (self.data[element['end']:element['end'] + 1] == ' '):
          self.boxing.append('space')
        
    elif self.version == '1.0.0':
      if (tag == 'br') or (tag == 'p'):
        if (len(self.boxing) > 0):
          self.boxing.append('newline')
      elif (tag == 'span') and (('class', 'ocr_line') in attrs):
        element = {}
        element['complete'] = re.search('{0}(.*?)</span>'.format(self.get_starttag_text()), self.data).group(0)
        
        if "<span class='ocr_cinfo'" not in element['complete']:
          return None
        
        element['text'] = re.search('">(.*)<span', element['complete']).group(1)
        element['positions'] = re.search('title="x_bboxes (.*) ">', element['complete']).group(1)
        element['positions'] = [int(item) for item in element['positions'].split()]

        i = 0
        
        for char in element['text']:
          section = element['positions'][i:i + 4]
          positions = {'char': char,
                       'xmin': section[0],
                       'ymin': section[1],
                       'xmax': section[2],
                       'ymax':section[3]}
          
          i += 4

          if (char == ' '):
            self.boxing.append('space')
            continue

          subst = {'"': '\\"',
                   "'":"\\'",
                   '\\': '\\\\'}
          
          if positions['char'] in subst.keys():
            positions['char'] = subst[positions['char']]
          
          self.boxing.append(positions)

    return None



class boxfileParser():
  def __init__(self):
    self.boxing = []
    self.image = ''

  def parse_box(self, boxfile):
    data = []

    for line in boxfile.split('\n'):
      if line == '':
        continue
      
      line = line.split()
      
      if len(line) != 5 and len(line) != 6:
        print('err: ocr.boxfileParser.parse_box(): The format of the boxfile is not what was expected.')
      
      data.append({'char': line[0],
                   'xmin': int(line[1]),
                   'ymin': int(line[2]),
                   'xmax': int(line[3]),
                   'ymax': int(line[4])})

    return data

  def resolve(self, boxdata, text):
    boxtext = ''
    
    for entry in boxdata:
      boxtext = boxtext + entry['char']

    text = text.replace(' ', '').replace('\n', '')

    diff = difflib.SequenceMatcher(None, boxtext, text)
    queue = []
    
    for action, a_start, a_end, b_start, b_end in diff.get_opcodes():
      entry = boxdata[a_start]
      item = {'action': action,
              'target': entry,
              'boxtext': boxtext[a_start:a_end],
              'text': text[b_start:b_end]}
      
      queue.append(item)

    for change in queue:
      if (change['action'] == 'replace'):
        if len(change['boxtext']) == 1 and len(change['text']) == 1:
          index = boxdata.index(change['target'])
          boxdata[index]['char'] = change['text']
        elif len(change['boxtext']) > 1 and len(change['text']) == 1:
          index = boxdata.index(change['target'])
          new = {'char': '', 
                 'xmin': 0,
                 'ymin': 0,
                 'xmax': 0,
                 'ymax': 0}
          
          new['char'] = change['text']
          
          for parameter in ['xmin', 'ymin', 'xmax', 'ymax']:
            new[parameter] = min([x[parameter] for x in boxdata[index:index + len(change['boxtext'])]])
          
          del(boxdata[index:index + len(change['boxtext'])])
          
          boxdata.insert(index, new)
        elif len(change['boxtext']) == 1 and len(change['text']) > 1:
          index = boxdata.index(change['target'])
          
          del(boxdata[index])
          
          i = 0
          
          for char in list(change['text']):
            new = {'char': char,
                   'xmin': change['target']['xmin'],
                   'ymin': change['target']['ymin'],
                   'xmax': change['target']['xmax'],
                   'ymax': change['target']['ymax']}
            
            boxdata.insert(index+i, new)
            i += 1
        elif len(change['boxtext']) > 1 and len(change['text']) > 1:
          if len(change['boxtext']) == len(change['text']):
            index = boxdata.index(change['target'])
            
            for char in list(change['text']):
              boxdata[index]['char'] = char
              index += 1
          else:
            index = boxdata.index(change['target'])
            deletions = boxdata[index:index + len(change['boxtext'])]
            
            for target in deletions:
              boxdata.remove(target)

            i = 0
            
            for char in list(change['text']):
              new = {'char': char,
                     'xmin': change['target']['xmin'],
                     'ymin': change['target']['ymin'],
                     'xmax': change['target']['xmax'],
                     'ymax': change['target']['ymax']}
              
              boxdata.insert(index + i, new)
              i += 1
      elif change['action'] == 'delete':
        index = boxdata.index(change['target'])
        deletions = boxdata[index:index + len(change['boxtext'])]
        
        for target in deletions:
          boxdata.remove(target)
      elif change['action'] == 'insert':
        index = boxdata.index(change['target'])
        i = 0
        
        for char in list(change['text']):
          new = {'char': char,
                 'xmin': change['target']['xmin'],
                 'ymin': change['target']['ymin'],
                 'xmax': change['target']['xmax'],
                 'ymax': change['target']['ymax']}
          
          boxdata.insert(index+i, new)
          i += 1

    return boxdata

  def parse(self, boxfile, text):
    boxfile = self.parse_box(boxfile)
    boxfile = self.resolve(boxfile, text)
    warning_count = 0

    for x in range(len(text)):
      char = text[x]
      
      if len(boxfile) == 0:
        break

      if char == '\n':
        if len(self.boxing) > 0 and self.boxing[-1] != 'newline':
          self.boxing.append('newline')
        continue
      elif char == ' ':
        if len(self.boxing) > 0 and self.boxing[-1] != 'space':
          self.boxing.append('space')
        continue
      else:
        if char != boxfile[0]['char']:
          if len(boxfile) >= 2 and x + 3 <= len(text):
            if text[x + 1] == boxfile[1]['char']:
              boxfile.pop(0)
            elif text[x] == boxfile[1]['char']:
              pass
            elif warning_count == 0:
              warning_count += 1
              print utils.color('wrn: tesseract produced a significant mismatch between textual data and character position data on "{0}".  This may result in partial ocr content for this page.'.format(os.path.split(self.image)[1]), 'red')
          continue
        
        if char in ['"', '\\']:
          boxfile.pop(0)
          continue
        
        self.boxing.append(boxfile.pop(0))

    return None


class djvuWordBox:
  def __init__(self):
    self.xmax = 0
    self.xmin = 100000
    self.ymax = 0
    self.ymin = 100000
    self.word = ''

  def add_char(self, boxing):
    if boxing['xmin'] < self.xmin: self.xmin = boxing['xmin']
    if boxing['ymin'] < self.ymin: self.ymin = boxing['ymin']
    if boxing['xmax'] > self.xmax: self.xmax = boxing['xmax']
    if boxing['ymax'] > self.ymax: self.ymax = boxing['ymax']
    
    self.word += boxing['char']
    
    return None

  def encode(self):
    if self.xmin > self.xmax or self.ymin > self.ymax:
      print('err: ocr.djvuWordBox(): Boxing information is impossible (x/y min exceed x/y max).')
    
    return '(word {0} {1} {2} {3} "{4}")'.format(self.xmin, self.ymin, self.xmax, self.ymax, self.word.encode('utf-8'))


class djvuLineBox:
  def __init__(self):
    self.xmax = 0
    self.xmin = 100000
    self.ymax = 0
    self.ymin = 100000
    self.words = []

  def add_word(self, word_box):
    if word_box.xmin < self.xmin: self.xmin = word_box.xmin
    if word_box.ymin < self.ymin: self.ymin = word_box.ymin
    if word_box.xmax > self.xmax: self.xmax = word_box.xmax
    if word_box.ymax > self.ymax: self.ymax = word_box.ymax
    
    self.words.append(word_box)

  def encode(self):
    if self.xmin > self.xmax or self.ymin > self.ymax:
      print 'err: ocr.djvuLineBox(): Boxing information is impossible (x/y min exceed x/y max).'
    
    words = '\n  '.join([x.encode() for x in self.words])
    
    return '(line {0} {1} {2} {3}\n  {4})'.format(self.xmin, self.ymin, self.xmax, self.ymax, words)


class djvuPageBox:
  def __init__(self):
    self.xmax = 0
    self.xmin = 100000
    self.ymax = 0
    self.ymin = 100000
    self.lines = []

  def add_line(self, line_box):
    if line_box.xmin < self.xmin: self.xmin = line_box.xmin
    if line_box.ymin < self.ymin: self.ymin = line_box.ymin
    if line_box.xmax > self.xmax: self.xmax = line_box.xmax
    if line_box.ymax > self.ymax: self.ymax = line_box.ymax
    
    self.lines.append(line_box)

  def encode(self):
    if self.xmin > self.xmax or self.ymin > self.ymax:
      print 'err: ocr.djvuPageBox(): Boxing information is impossible (x/y min exceed x/y max).'
    
    lines = '\n  '.join([x.encode() for x in self.lines])
    
    return '(page {0} {1} {2} {3}\n  {4})'.format(self.xmin, self.ymin, self.xmax, self.ymax, lines)


class OCR:
  def __init__(self, opts):
    self.opts = opts
    self.dep_check()

  def _cuneiform(self, filename):
    status = utils.simple_exec('cuneiform -f hocr -o "{0}.hocr" {1} "{0}"'.format(filename, self.opts['cuneiform_options']))
    
    if status != 0:
      if status == -6:
        print utils.color('\nwrn: cuneiform encountered a buffer overflow on "{0}".  Ocr on this image will be done with tesseract.'.format(os.path.split(filename)[1]), 'red')
      else:
        print utils.color('wrn: cuneiform crashed on "{0}".  Ocr on this image will be done with tesseract.'.format(os.path.split(filename)[1]), 'red')
      
      return self._tesseract(filename)

    text = codecs.codecs.open('{0}.hocr'.format(filename), 'r', encoding = 'utf8').read()
    basename = '.'.join(os.path.split(filename)[1].split('.')[:-1])
    
    if os.path.isdir(basename + '_files'):
      shutil.rmtree(basename + '_files')
    
    os.remove(filename + '.hocr')

    parser = hocrParser()
    parser.parse(text)

    height = int(utils.execute('identify -format %H "{0}"'.format(filename), capture = True))
    
    for entry in parser.boxing:
      if entry not in ['space', 'newline']:
        ymin, ymax = entry['ymin'], entry['ymax']
        entry['ymin'] = height - ymax
        entry['ymax'] = height - ymin

    return parser.boxing

  def _tesseract(self, filename):
    basename = os.path.split(filename)[1].split('.')[0]
    tesseractpath = utils.get_executable_path('tesseract')
    
    status_a = utils.simple_exec('{0} "{1}" "{2}_box" {3} batch makebox'.format(tesseractpath, filename, basename, self.opts['ocr_options']))
    status_b = utils.simple_exec('{0} "{1}" "{2}_txt" {3} batch'.format(tesseractpath, filename, basename, self.opts['ocr_options']))
    
    if status_a != 0 or status_b != 0:
      print utils.color('wrn: Tesseract failed on "{0}".  There will be no ocr for this page.'.format(os.path.split(filename)[1]), 'red')
      return []

    if os.path.exists(basename + '_box.txt'):
      boxfilename = basename + '_box.txt'
    else:
      boxfilename = basename + '_box.box'

      boxfile = codecs.open(boxfilename, 'r', encoding = 'utf8').read()
      textfile = codecs.open(basename+'_txt.txt', 'r', encoding = 'utf8').read()

    os.remove(boxfilename)
    os.remove(basename + '_txt.txt')

    parser = boxfileParser()
    parser.image = filename
    parser.parse(boxfile, textfile)

    return parser.boxing

  def analyze_image(self, filename):
    if self.opts['ocr_engine'] == 'tesseract':
      boxing = self._tesseract(filename)
    elif self.opts['ocr_engine'] == 'cuneiform':
      boxing = self._cuneiform(filename)
    else:
      print 'wrn: ocr engine "{0}" is not supported.'.format(self.opts['ocr_engine'])

    return boxing

  def dep_check(self):
    engine = self.opts['ocr_engine']

    if not utils.is_executable(engine):
      print utils.color('wrn: ocr engine "{0}" is not installed. Tesseract will be used instead.'.format(engine), 'red')
      self.opts['ocr_engine'] = 'tesseract'
    
    if engine != 'tesseract' and not utils.is_executable('tesseract'):
      print 'err: ocr engine "{0}" is not installed.  Tesseract is a mandatory dependency.'.format('tesseract')

    return None

  def translate(self, boxing):
    page = djvuPageBox()
    line = djvuLineBox()
    word = djvuWordBox()
    
    for entry in boxing:
      if entry == 'newline':
        if line.words != []:
          if word.word != '':
            line.add_word(word)
          page.add_line(line)
        line = djvuLineBox()
        word = djvuWordBox()
      elif entry == 'space':
        if word.word != '':
          line.add_word(word)
        word = djvuWordBox()
      else:
        word.add_char(entry)
    
    if word.word != '':
      line.add_word(word)
    
    if line.words != []:
      page.add_line(line)

    if page.lines != []:
      return page.encode()
    else:
      return ''
