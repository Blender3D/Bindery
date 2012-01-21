try:
  import ConfigParser as ConfigParser
except ImportError:
  import configparser as ConfigParser

class config:
  def __init__(self, filename):
    self.filename = filename
    
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.filename)
  
  def get(self, section, name):
    return self.config.get(section, name)
  
  def set(self, section, name, value):
    self.config.set(section, name, value)
    self.config.write(open(self.filename, 'wb'))

class config:
  def __init__(self, filename):
    self.filename = filename
    
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.filename)
  
  def get(self, section, name):
    return ''
  
  def set(self, section, name, value):
    pass
