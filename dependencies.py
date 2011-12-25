import os, sys
import platform

class Package:
  def __init__(self, name = None, version = None, binary = None):
    self.name = None
    self.version = None
    self.test_binary = None
  
  def exists(self):
    if sys.platform.startswith('win'):
      pathext = os.environ['PATHEXT']
    else:
      pathext = ''

    for path in os.environ['PATH'].split(os.pathsep):
      if os.path.isdir(path):
        for ext in pathext.split(os.pathsep):
          name = os.path.join(path, command + ext)
          
          if os.access(name, os.X_OK) and not os.path.isdir(name):
            return True
            
    return False
  
  def install(self):
    name = platform.dist()[0].lower()
    
    if 'bunu' in name:
      package_manager = 'apt-get install {0}'
    elif any(word in name for word in ['fedora', 'red hat', 'yellow']):
      package_manager = 'yum install {0}'
    
  
for command in ['python', 'djvm', 'minidjvu', 'jbig2']:
  print is_installed(command)
