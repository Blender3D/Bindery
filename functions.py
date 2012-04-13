import sys, os, time, glob, re, tempfile

try:
  from djvubind import utils
except:
  from binding.djvubind import utils

from ui.BookListWidget import BookListWidget, BookListWidgetItem

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
  # Pynotify makes Qt4 segfault. Why?
  import pynotify
  pynotify.init('Bindery')
  
  notify = True
except:
  notify = False


def all_same(items):
  return all(x == items[0] for x in items)



class StartQT4(QMainWindow):
  def injectWindowsPath(self):
    try:
      import win32api, win32con
      
      def getenv_system(name):
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment')
        value = win32api.ExpandEnvironmentStrings(str(win32api.RegQueryValueEx(key, name)[0]))
        win32api.RegCloseKey(key)
        
        return value

      def setenv_system(name, value):
        key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 0, win32con.KEY_WRITE)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, value)
        win32api.RegCloseKey(rkey)
      
      self.windows_path = getenv_system('PATH').split(';')
      
      if os.path.abspath('bin/') not in self.windows_path:
        setenv_system('PATH', ';'.join([os.path.abspath('bin/')] + self.windows_path)
    except:
      pass
  
  def restoreWindowsPath(self):
    if self.windows_path:
      setenv_system('PATH', ';'.join(self.windows_path)
  
  def checkDependencies(self):
    self.injectWindowsPath()
    
    ocr_engines = [str(self.ui.ocrEngine.itemText(index)) for index in range(self.ui.ocrEngine.count())]
    installed_ocr_engines = []
    
    for index, engine in enumerate(ocr_engines):
      if utils.is_executable(engine.lower()):
        installed_ocr_engines.append(engine)
      else:
        self.ui.ocrEngine.removeItem(index)
    
    if not installed_ocr_engines:
      self.ui.tabWidget.removeTab(2)
    
    
    if not utils.is_executable('pdfbeads'):
      self.ui.outputFormat.removeItem(1)
  
  
  
  def previewPage(self, image):
    if self.ui.pagePreview.scene():
      self.ui.pagePreview.scene().clear()
      self.ui.pagePreview.scene().addPixmap(QPixmap().fromImage(image))
    else:
      scene = QGraphicsScene()
      scene.addPixmap(QPixmap().fromImage(image))
      self.ui.pagePreview.setScene(scene)
  
  
  
  def itemSelectionChanged(self):
    self.selected = self.ui.pageList.selectedItems()
    
    if self.selected:
      self.ui.pageTab.setEnabled(True)
      
      for widget in [self.ui.removePageButton, self.ui.removePageMenuItem]:
        print(len(self.selected))
        widget.setEnabled(len(self.selected) > 0)
      
      self.ui.singlePageFrame.setEnabled(len(self.selected) == 1)
      
      if len(self.selected) == 1:
        row = self.ui.pageList.row(self.selected[0])
        
        self.ui.moveToTopButton.setEnabled(row != 0)
        self.ui.moveUpButton.setEnabled(row != 0)
        
        self.ui.moveToBottomButton.setEnabled(row != self.ui.pageList.count() - 1)
        self.ui.moveDownButton.setEnabled(row != self.ui.pageList.count() - 1)
        
        self.previewer.image = self.selected[0].path
        self.previewer.size = [self.ui.pagePreview.size().width() * 2, self.ui.pagePreview.size().width() * 2]
        self.previewer.start()
    else:
      self.ui.pageTab.setEnabled(False)
  
  
  
  def pageGrayscaleChanged(self, state):
    if state == Qt.PartiallyChecked:
      state = Qt.Checked
      self.ui.pageGrayscale.setCheckState(Qt.Checked)
    
    for page in self.ui.pageList.selectedItems():
      page.grayscale = (state == Qt.Checked)
  
  
  
  def makeIcon(self, index, icon):
    item = self.ui.pageList.item(index)
    item.setIcon(QIcon(QPixmap.fromImage(icon)))
  
  
  
  def outputFormatChanged(self, choice):
    folder, filename = os.path.split(str(self.ui.outputFile.text()))
    basename, extension = os.path.splitext(filename)
    
    self.ui.outputFile.setText(os.path.join(folder, basename + '.' + str(self.ui.outputFormat.currentText()).lower()))
    self.ui.stackedWidget.setCurrentIndex(choice)
  
  
  
  def hideBackground(self):
    if self.ui.pageList.count() > 0:
      self.ui.pageList.setStyleSheet('')
    else:
      self.ui.pageList.setStyleSheet(
        '''QListWidget {
          background-image: url(':/icons/go-down-big.png');
          background-position: center;
          background-repeat: no-repeat;
          background-color: white;
        }

        QListWidget:hover {
          background-image: url(':/icons/go-down-big-hover.png');
          background-position: center;
          background-repeat: no-repeat;
          background-color: white;
        }'''
      )
  

  
  def addToProject(self):
    for item in self.projectFilesUi.offProjectList.selectedItems():
      self.projectFilesUi.offProjectList.takeItem(self.projectFilesUi.offProjectList.row(item))
      self.projectFilesUi.inProjectList.addItem(item)


  
  def removeFromProject(self):
    for item in self.projectFilesUi.inProjectList.selectedItems():
      self.projectFilesUi.inProjectList.takeItem(self.projectFilesUi.inProjectList.row(item))
      self.projectFilesUi.offProjectList.addItem(item)
  
  
  def addFile(self, filename, index=None, title=None):
    filename = str(filename)
    
    if os.path.splitext(os.path.split(filename)[-1])[-1] in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
      item = BookListWidgetItem(os.path.split(filename)[-1] if not title else title, filename)
      
      if filename not in [str(self.ui.pageList.item(i).path) for i in range(self.ui.pageList.count())]:
        if index:
          self.ui.pageList.insertItem(index, item)
        else:
          self.ui.pageList.addItem(item)
        
        return True
    
    return False
  
  
  
  def filesDropped(self, files):
    for filename in files:
      self.addFile(filename)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
  
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      self.thumbnailer.start()
  
  
  
  def changeOCRLanguage(self, language):
    currentOptions = str(self.ui.ocrOptions.text())
    arguments = currentOptions.split(' ')
    
    if '-l' in currentOptions:
      for i in range(len(arguments) - 1):
        if arguments[i] == '-l':
          arguments[i + 1] = str(language).lower()[:3]
          break
      
      self.ui.ocrOptions.setText(' '.join(arguments))
    else:
      self.ui.ocrOptions.setText('-l {0}'.format(language.toLower()[:3]))
  
  
  def projectFilesAccepted(self):
    self.ui.outputFile.setText(self.projectFilesUi.outputFile.text())
    
    if self.projectFilesUi.inProjectList.count() == 0:
      QMessageBox.warning(self, '', 'There are no pages to process.\nPlease add them using the green arrows.', QMessageBox.Ok, QMessageBox.Ok)
    elif self.ui.outputFile.text() == '':
      QMessageBox.warning(self, '', 'No output file has been selected.\nPlease select one using the "Output File" form.', QMessageBox.Ok, QMessageBox.Ok)
    else:
      self.projectFiles.close()
      
      for i in range(self.projectFilesUi.inProjectList.count()):
        orig = self.projectFilesUi.inProjectList.item(i)
        item = BookListWidgetItem(str(orig.text()), str(orig.statusTip()))
        
        if orig.text() not in [str(self.ui.pageList.item(i).text()) for i in range(self.ui.pageList.count())]:
          self.ui.pageList.addItem(item)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
    
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      self.thumbnailer.start()
  
  
  
  def removeFiles(self):
    for item in self.ui.pageList.selectedItems():
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
    
    self.hideBackground()
  
  
  
  def togglePreviews(self, on=True):
    self.previews = on
    
    if on:
      self.thumbnailer.die = False
      
      while self.thumbnailer.isRunning():
        time.wait(0.1)
      
      for i in range(self.ui.pageList.count()):
        self.ui.pageList.item(i).resetIcon()
      
      self.thumbnailer.start()
    else:
      self.thumbnailer.die = True
  
  
  
  def updateProgress(self, value, message):
    self.ui.progressBar.setValue(value)
    self.ui.progressBar.setFormat('{0} - %p%'.format(message))
  
  
  
  def updateBackground(self, item, color):
    self.ui.pageList.item(item).setBackground(color)
  
  
  
  def clearDebugLog(self):
    if QMessageBox.question(self, '', 'Are you sure you want to clear the debug log?', QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
      self.ui.debugLog.clear()
  
  
  
  def finishedBinding(self):
    self.ui.progressBar.reset()
    
    self.ui.startButton.setText('Start')
    self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-start'))
    
    if notify:
      notification = pynotify.Notification('Bindery', 'Your book has finished binding', 'ui/icons/logo.png')
      notification.show()
    else:
      QMessageBox.information(self, '', 'Your book has finished binding.', QMessageBox.Ok, QMessageBox.Ok)
    
    for i in range(self.ui.pageList.count()):
      self.ui.pageList.item(i).setBackground(QColor(0, 0, 0, 0))
  
  
  def toggleBinding(self):
    if str(self.ui.startButton.text()) == 'Start':
      if self.ui.outputFile.text() == '':
        self.showSaveDialog()
      
      self.pages = [self.ui.pageList.item(i) for i in range(self.ui.pageList.count())]
    
      self.ui.startButton.setText('Stop')
      self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-stop'))
      self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-stop'))
      
      self.options = {
        'output_file':       str(self.ui.outputFile.text()),
        'ocr':               (self.ui.enableOCR.checkState() == Qt.Checked),
        'ocr_engine':        str(self.ui.ocrEngine.currentText()).lower(),
        'output_format':     str(self.ui.outputFormat.currentText()).lower(),
        'tesseract_options': str(self.ui.ocrOptions.text()),
        'cuneiform_options': str(self.ui.ocrOptions.text()),
        'color_encoder':     str(self.ui.djvuColorEncoder.currentText()),
        'c44_options':       str(self.ui.c44Options.text()),
        'cjb2_options':      str(self.ui.cjb2Options.text()),
        'cpaldjvu_options':  str(self.ui.cpaldjvuOptions.text()),
        'csepdjvu_options':  str(self.ui.csepdjvuOptions.text()),
        'minidjvu_options':  str(self.ui.minidjvuOptions.text()),
        'numbering_type':    [],
        'numbering_start':   [],
        'title':             str(self.ui.bookTitle.text()),
        'author':            str(self.ui.bookAuthor.text()),
        'subject':           str(self.ui.bookSubject.text()),
        'keywords':           str(self.ui.bookKeywords.text()),
        'win_path':          'C:\\Program Files\\DjVuZone\\DjVuLibre\\'
      }
      
      if self.options['output_format'] == 'djvu':
        self.options['bitonal_encoder'] = str(self.ui.djvuBitonalEncoder.currentText())
      elif self.options['output_format'] == 'pdf':
        self.options['background_encoder'] = re.sub(r'\s+\(.*?\)', '', str(self.ui.pdfBackgroundEncoder.currentText()))
        self.options['page_layout'] = str(self.ui.pdfPageLayout.currentText()).replace(' ', '')
        self.options['foreground_encoder'] = str(self.ui.pdfForegroundEncoder.currentText())
        self.options['pages_per_dict'] = self.ui.jbig2DictionarySize.value()
        self.options['binarization_threshold'] = self.ui.binarizationThreshold.value()
        self.options['max_indexed_colors'] = self.ui.maxIndexedColors.value()
      
      if os.path.isfile(self.options['output_file']):
        os.remove(self.options['output_file'])
      
      self.binder.initialize(self.pages, self.options)
      self.binder.start()
    else:
      self.binder.die = True
      self.binder.terminate()
      self.ui.progressBar.reset()
      
      self.ui.startButton.setText('Start')
      self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-start'))
      self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-start'))
      
      for i in range(self.ui.pageList.count()):
        self.ui.pageList.item(i).setBackground(QColor(0, 0, 0, 0))
