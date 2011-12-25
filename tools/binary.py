#!/usr/bin/env python

import os
import sys
import shutil

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [parent_dir] + sys.path

try:
  from cx_Freeze import setup, Executable
except ImportError:
  sys.exit('cx_Freeze must be installed to use this script')

if sys.platform.startswith('win'):
  try:
    from win32verstamp import stamp
  except ImportError:
    from time import sleep
    print '*** WARNING ***'
    print 'the script will be unable to create the version resource'
    print 'install pywin32 extensions if you want the file stamped'
    sleep(2)


def qt4_plugins_dir():
  from PyQt4.QtCore import QCoreApplication
  app = QCoreApplication([])

  qt4_plugin_dirs = map(unicode, app.libraryPaths())
  
  if not qt4_plugin_dirs:
    return
  for d in qt4_plugin_dirs:
    if os.path.isdir(d):
      return str(d)

qt4_plugin_dir = qt4_plugins_dir()

if qt4_plugin_dir is None:
  sys.exit('Cannot find PyQt4 plugins directory')


includes = [
  'atexit',
  'PyQt4.QtSvg',
  'PyQt4.QtXml'
]

include_files = [
  [os.path.join(qt4_plugin_dir, 'imageformats'), 'imageformats']
]


exe = Executable(
  script = os.path.join(parent_dir, 'main.py'),
  icon = os.path.join(parent_dir, 'ui/icons/logo.ico')
)


setup(
  name = 'Bindery',
  version = '0.9.0',
  description = 'A simple GUI for binding post processed scanned pages into digital documents',
  options = {'build_exe': {'includes': includes, 'include_files': include_files}},
  executables = [exe]
)

shutil.move('build', 'bindery')
shutil.copy('launcher.exe', os.path.join('bindery', 'Bindery.exe'))
shutil.copytree(os.path.join(parent_dir, 'bin'), os.path.join('bindery', 'bin'))
shutil.copy(os.path.join(parent_dir, 'options.ini'), os.path.join('bindery', 'options.ini'))
os.system('7za.exe a -tzip "bindery.zip" "bindery"')
shutil.move('bindery', 'build')