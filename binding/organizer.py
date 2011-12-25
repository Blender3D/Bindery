import os
import sys

import utils

class Book:
  def __init__(self):
    self.pages = []
    self.suppliments = {'cover_front': None,
                        'cover_back': None,
                        'metadata': None,
                        'bookmarks': None
                       }
    self.dpi = None

  def get_dpi(self):
    for page in self.pages:
      if self.dpi is not None and page.dpi != self.dpi:
        print 'wrn: {0}'.format(page.path)
        print 'wrn: organizer.Book.analyze(): Page dpi is different from the previous page.'
        print 'wrn: organizer.Book.analyze(): If you encounter problems with minidjvu, this is probably why.'
      
      self.dpi = page.dpi
    
    return None

  def insert_page(self, path):
    self.pages.append(Page(path))
    
    return None

class Page:
  def __init__(self, path):
    self.path = os.path.abspath(path)

    self.bitonal = None
    self.make_grayscale = False
    self.dpi = 0
    self.text = ''

  def get_dpi(self):
    self.dpi = int(utils.execute('identify -ping -format %x "{0}"'.format(self.path), capture = True).decode('ascii').split(' ')[0])
    return None

  def is_bitonal(self):
    print 'identify -ping "{0}"'.format(self.path)
	
    if utils.execute('identify -ping "{0}"'.format(self.path), capture = True).decode('ascii').find('Bilevel')  ==  -1:
      self.bitonal = False
    else:
      if (utils.execute('identify -ping -format %z "{0}"'.format(self.path), capture = True).decode('ascii') !=  ('1' + os.linesep)):
        print("msg: {0}: Bitonal image but with a depth greater than 1.  Modifying image depth.".format(os.path.split(self.path)[1]))
        utils.execute('mogrify -colors 2 "{0}"'.format(self.path))
      self.bitonal = True
    return None
