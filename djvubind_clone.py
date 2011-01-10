import optparse
import os
import queue
import shutil
import sys
import threading
import time

import encode
import ocr
import organizer
import utils

class djvuAnalyze:
  def __init__(self, queue):
    self.queue = reversed(queue)
    self.quit = False
  
  def run(self):
    while not self.quit:
      if len(self.queue) == 0:
        self.quit = True
        break
      
      page = self.queue[-1]
      page.is_bitonal()
      page.get_dpi()




class djvuOCR:
  def __init__(self, queue, ocr):
    self.queue = reversed(queue)
    self.ocr = ocr
    
    self.quit = False
  
  def run(self):
    while not self.quit:
    if len(self.queue) == 0:
      self.quit = True
      break
      
      page = self.queue[-1]
      boxing = self.ocr.analyze_image(page.path)
      page.text = self.ocr.translate(boxing)










class Project:
  """
  Abstraction of the entire project.  This should make things like status
  reports, clean exits on errors, and access to information a little easier.
  """

  def __init__(self, opts):
    self.get_config(opts)

    self.out = 'book.djvu'

    self.book = djvubind.organizer.Book()
    self.enc = djvubind.encode.Encoder(self.opts)
    self.ocr = djvubind.ocr.OCR(self.opts)

  def add_file(self, filename, type='page'):
    """
    Adds a file to the project.
    type can be 'page', 'cover_front', 'cover_back', 'metadata', or 'bookmarks'.
    """

    # Check that type is valid and file exists.
    if type not in ['page', 'cover_front', 'cover_back', 'metadata', 'bookmarks']:
      msg = 'err: Project.add_file(): type "{0}" is unknown.'.format(type)
      print(msg)
      sys.exit(1)
    if not os.path.isfile(filename):
      msg = 'err: Project.add_file(): "{0}" does not exist or is not a file.'.format(filename)
      print(msg)
      sys.exit(1)

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

    # Create queu and populate with pages to process
    q = queue.Queue()
    for i in self.book.pages:
      q.put(i)

    # Create threads to process the pages in queue
    print('  Spawning {0} processing threads.'.format(self.opts['cores']))
    for i in range(self.opts['cores']):
      p = ThreadAnalyze(q)
      p.daemon = True
      p.start()

    # Wait for everything to digest.  Note that we don't simply call q.join()
    # because it blocks, preventing something like ctrl-c from killing the program.
    pagecount = len(self.book.pages)
    while not q.empty():
      try:
        time.sleep(3)
        # Report completion percentage.
        # N.b., this is perfect, since queue.qsize() isn't completely reliable in a threaded
        # environment, but it will do well enough to give the user and idea of where we are.
        position = ( (pagecount - q.qsize() - self.opts['cores']) / pagecount ) * 100
        print('  {0:.2f}% completed.     '.format(position), end='\r')
      except KeyboardInterrupt:
        print('')
        sys.exit(1)
    q.join()

    return None

  def bind(self):
    """
    Fully encodes all images into a single djvu file.  This includes adding
    known ocr information, covers, metadata, etc.
    """

    self.enc.enc_book(self.book, self.out)

    return None

  def get_config(self, opts):
    """
    Retrives configuration options set in the user's config file.  Options
    passed through the command line (already in 'opts') should be
    translated and overwrite config file options.
    """

    # Set default options
    self.opts = {'cores':-1,
           'ocr':True,
           'ocr_engine':'tesseract',
           'cuneiform_options':'',
           'tesseract_options':'',
           'bitonal_encoder':'cjb2',
           'color_encoder':'csepdjvu',
           'c44_options':'',
           'cjb2_options':'-lossy',
           'cpaldjvu_options':'',
           'csepdjvu_options':'',
           'minidjvu_options':'--match -pages-per-dict 100',
           'numbering_type':[],
           'numbering_start':[],
           'win_path':'C:\\Program Files\\DjVuZone\\DjVuLibre\\'}

    # Load the global config file first
    if not sys.platform.startswith('win'):
      filename = '/etc/djvubind/config'
      if os.path.isfile(filename):
        config_opts = djvubind.utils.parse_config(filename)
        self.opts.update(config_opts)

    # Load the options from the user's config file, if it exists.
    if sys.platform.startswith('win'):
      filename = os.path.expanduser('~\\Application Data\\djvubind\\config')
    else:
      filename = os.path.expanduser('~/.config/djvubind/config')
    filename = os.path.normpath(filename)
    if os.path.isfile(filename):
      config_opts = djvubind.utils.parse_config(filename)
      self.opts.update(config_opts)
    else:
      if os.path.isfile('/etc/djvubind/config'):
        conf_dir = os.path.expanduser('~/.config/djvubind')
        if not os.path.isdir(conf_dir):
          os.makedirs(conf_dir)
        shutil.copy('/etc/djvubind/config', filename)
        config_opts = djvubind.utils.parse_config(filename)
        self.opts.update(config_opts)
      else:
        msg = 'msg: Project.get_config(): No user config file found ({0}).'.format(filename)
        msg = msg + '\n' + 'A sample config file is included in the source (docs/config).'
        print(msg)


    # Set cetain variables to the proper type
    self.opts['cores'] = int(self.opts['cores'])
    self.opts['ocr'] = (self.opts['ocr'] == 'True')

    # Overwrite or create values for certain command line options
    if opts.no_ocr:
      self.opts['ocr'] = False
    if opts.ocr_engine is not None:
      self.opts['ocr_engine'] = opts.ocr_engine
    if opts.tesseract_options is not None:
      self.opts['tesseract_options'] = opts.tesseract_options
    if opts.cuneiform_options is not None:
      self.opts['cuneiform_options'] = opts.cuneiform_options
    if opts.numbering_type is not None:
      self.opts['numbering_type'] = opts.numbering_type
    if opts.numbering_start is not None:
      self.opts['numbering_start'] = [int(item) for item in opts.numbering_start]
    self.opts['verbose'] = opts.verbose
    self.opts['quiet'] = opts.quiet

    # Detect number of cores if not manually set already
    if self.opts['cores'] == -1:
      self.opts['cores'] = djvubind.utils.cpu_count()

    # Update windows PATH so that we can find the executable we need.
    if sys.platform.startswith('win'):
      if self.opts['win_path'] != '':
        os.environ['PATH'] = '{0};{1}'.format(self.opts['win_path'], os.environ['PATH'])

    if self.opts['verbose']:
      print('Executing with these parameters:')
      print(self.opts)
      print('')

    return None

  def get_ocr(self):
    """
    Performs optical character analysis on all images, excluding covers.
    """

    if not self.opts['ocr']:
      print('  OCR is disabled and will be skipped.')
      return None

    # Create queu and populate with pages to process
    q = queue.Queue()
    for i in self.book.pages:
      q.put(i)

    # Create threads to process the pages in queue
    print('  Spawning {0} processing threads.'.format(self.opts['cores']))
    for i in range(self.opts['cores']):
      p = ThreadOCR(q, self.ocr)
      p.daemon = True
      p.start()

    # Wait for everything to digest.  Note that we don't simply call q.join()
    # because it blocks, preventing something like ctrl-c from killing the
    # program.
    pagecount = len(self.book.pages)
    while not q.empty():
      try:
        time.sleep(3)
        # Report completion percentage.
        # N.b., this is perfect, since queue.qsize() isn't completely reliable in a threaded
        # environment, but it will do well enough to give the user and idea of where we are.
        position = ( (pagecount - q.qsize() - self.opts['cores']) / pagecount ) * 100
        print('  {0:.2f}% completed.     '.format(position), end='\r')
      except KeyboardInterrupt:
        print('')
        sys.exit(1)
    q.join()

    return None


if __name__ == '__main__':
  version = '1.0.2'

  # Command line parsing
  usage = "usage: %prog [options] directory"
  description = "djvubind is designed to facilitate creating high-quality djvu files, including positional ocr, metadata, and bookmarks."
  parser = optparse.OptionParser(usage, version=version, description=description)
  parser.set_defaults(quiet=False, verbose=False,
            no_ocr=False, ocr_engine=None, tesseract_options=None, cuneiform_options=None,
            cover_front='cover_front.jpg', cover_back='cover_back.jpg',
            metadata='metadata', bookmarks='bookmarks',
            numbering_type=None, numbering_start=None)
  parser.add_option("--cover-front", dest="cover_front", help="Specifies an alternate front cover image.  By default, '%default' is used if present.")
  parser.add_option("--cover-back", dest="cover_back", help="Specifies an alternate back cover image.  By default, '%default' is used if present.")
  parser.add_option("--ocr-engine", dest="ocr_engine", help="Select which ocr engine to use (cuneiform|tesseract).  By default, '%default' is used.")
  parser.add_option("--tesseract-options", dest="tesseract_options", help="Additional command line options to pass to tesseract.")
  parser.add_option("--cuneiform-options", dest="cuneiform_options", help="Additional command line options to pass to cuneiform.")
  parser.add_option("--metadata", dest="metadata", help="Specifies an alternate metadata file.  By default, '%default' is used if present.")
  parser.add_option("--bookmarks", dest="bookmarks", help="Specifies an alternate bookmarks file.  By default, '%default' is used if present.")
  parser.add_option("--numbering-type", dest="numbering_type", action="append", help="")
  parser.add_option("--numbering-start", dest="numbering_start", action="append", help="")
  parser.add_option("--no-ocr", action="store_true", dest="no_ocr", help="Images will not be processed for text content.")
  parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
  parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
  (options, args) = parser.parse_args(sys.argv)

  if options.quiet:
    sys.stdout = open(os.devnull, 'w')
  if options.verbose:
    print('djvubind version {0} on {1}'.format(version, sys.platform))

  # Sanity checks on command line arguments and options
  if len(args) == 2:
    if not os.path.isdir(args[1]):
      print('The argument ({0}) is not a directory.'.format(args[1]))
      sys.exit(1)
  elif (len(args) > 2):
    print('Too many arguments, check your command syntax.')
    sys.exit(1)

  # Project needs to be initialized before doing dependency checks, since the
  # configuration file may supply PATH updates for Window environments.
  proj = Project(options)

  # Dependency check
  # N.B. checks for ocr engines *should* take place in ocr.OCR(), since which
  # ones are needed requires knowledge of config preferences, bitonal/nonbitonal, etc.
  # Likewise for encoders other than djvulibre tools (albeit in encode.Encode())
  deps = ['cpaldjvu', 'cjb2', 'djvm', 'djvused', 'identify']
  for dep in deps:
    if (not djvubind.utils.is_executable(dep)):
      print('err: __main__: external dependency ({0}) cannot be found.'.format(dep))
      sys.exit(1)

  # Increment the file name if a previous book.djvu already exists.
  i = 0
  while os.path.isfile(proj.out):
    i = i + 1
    proj.out = 'book(' + str(i) + ').djvu'

  # Add files to the project
  print('{0} Collecting files to be processed.'.format(djvubind.utils.color('*', 'green')))
  if os.path.isfile(options.cover_front):
    proj.add_file(options.cover_front, 'cover_front')
  if os.path.isfile(options.cover_back):
    proj.add_file(options.cover_back, 'cover_back')
  if os.path.isfile(options.metadata):
    proj.add_file(options.metadata, 'metadata')
  if os.path.isfile(options.bookmarks):
    proj.add_file(options.bookmarks, 'bookmarks')
  for filename in djvubind.utils.list_files():
    ext = filename.split('.')[-1]
    ext = ext.lower()
    if (ext in ['tif', 'tiff']) and (filename not in [options.cover_front, options.cover_back]):
      proj.add_file(filename, 'page')

  print('{0} Analyzing image information.'.format(djvubind.utils.color('*', 'green')))
  proj.analyze()
  proj.book.get_dpi()

  print('{0} Performing optical character recognition.'.format(djvubind.utils.color('*', 'green')))
  proj.get_ocr()

  print('{0} Encoding all information to {1}.'.format(djvubind.utils.color('*', 'green'), proj.out))
  proj.bind()
