import os, tempfile
from djvubind import utils, organizer

class Book(organizer.Book):
  def __init__(self):
    organizer.Book.__init__(self)
  
  def insert_page(self, path):
    self.pages.append(Page(path))
    
    return None

class Page(organizer.Page):
  def __init__(self, path=None):
    organizer.Page.__init__(self, path)
    
    self.width = None
    self.height = None
    
    self.textual = None
    self.graphical = None
    
    self.temporary = False
    self.grayscale = False
  
  def delete(self):
    if not self.temporary:
      return False

    return os.remove(self.path)
  
  def get_size(self):
    self.width, self.height = map(int, utils.execute('identify -ping -format %wx%h "{0}"'.format(self.path), capture=True).decode('ascii').split('x'))
    
    return self.width, self.height

  def is_bitonal(self):
    if utils.execute('identify -ping "{0}"'.format(self.path), capture=True).decode('utf8').find('Bilevel') == -1:
      self.bitonal = False
    else:
      if utils.execute('identify -ping -format %z "{0}"'.format(self.path), capture=True).decode('utf8') != '1' + os.linesep:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        
        utils.execute('convert "{0}" -colors 2 "{1}"'.format(self.path, temp.name))
        self.temporary = True
        self.path = temp.name
      
      self.bitonal = True
    
    return self.bitonal