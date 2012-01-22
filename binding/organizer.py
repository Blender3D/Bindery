from djvubind import utils, organizer

class Book(organizer.Book):
  def __init__(self):
    super().__init__()
  
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
    
    self.grayscale = False
    
  def get_size(self):
    self.width, self.height = map(int, utils.execute('identify -ping -format %wx%h "{0}"'.format(self.path), capture = True).decode('ascii').split('x'))
    
    return [self.width, self.height]
