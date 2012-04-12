from py2exe.build_exe import py2exe
from distutils.core import setup

def files(folder):
  for path in glob.glob(folder + '/*'):
    if os.path.isfile(path):
      yield path

data_files = [
  'bin/', files('bin'),
  'ui/', files('ui')
]

setup(
  zipfile = None,
  windows = [{'script': 'main.py'}],
  options = {
    'py2exe': {
	    'bundle_files': 1,
	    'includes': ['sip'],
      'dll_excludes': ['MSVCP90.dll']
	  }
  }
)
