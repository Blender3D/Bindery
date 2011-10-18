import sys, os, time, glob

import project_files
import config

from gui import *
from BookListWidget import * 
from thumbnailer import *
from bind import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
  import pynotify
  pynotify.init('Bindery')
except:
  pass

class StartQT4(QMainWindow):
  def itemSelectionChanged(self):
    self.selected = self.ui.pageList.selectedItems()
    self.ui.removePageButton.setEnabled(len(self.selected) > 0)
  
  
  
  def pageGrayscaleChanged(self, state):
    self.ui.pageList.selectedItems()[0].grayscale = (state == 2)
  
  
  
  def makeIcon(self, index, icon):
    item = self.ui.pageList.item(index)
    item.setIcon(QIcon(QPixmap.fromImage(icon)))
    
    self.ui.statusBar.showMessage('Thumbnailing ' + os.path.split(str(item.filepath))[1], 500)
  
  
  
  def hideBackground(self):
    if self.ui.pageList.count() > 0:
      self.ui.pageList.setStyleSheet('')
    else:
      self.ui.pageList.setStyleSheet('QListWidget\n{\nbackground-image: url(\':/icons/go-down-big.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}\n\nQListWidget:hover\n{\nbackground-image: url(\':/icons/go-down-big-hover.png\');\nbackground-position: center;\nbackground-repeat: no-repeat;\nbackground-color: white;\n}')
  
  
  
  def showProjectDialog(self):  self.projectFiles.show()    



  def showFileDialog(self):
    directory = QFileDialog.getExistingDirectory(self, 'Input directory', self.config.get('startup', 'input_directory'))
    
    if str(directory) != '':
      self.projectFilesUi.inputDirectory.setText(str(directory) + '/')
      
      self.config.set('startup', 'input_directory', str(directory) + '/')
      
      for file in glob.glob(str(directory) + '/*.*'):
        item = QListWidgetItem(os.path.split(file)[-1])
        item.setStatusTip(file)
        
        if os.path.splitext(os.path.split(file)[-1])[-1] not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
          item.setFlags(Qt.NoItemFlags)
        
        self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def showSaveDialog(self):
    self.outFile = QFileDialog.getSaveFileName(self, 'Save output file', self.config.get('startup', 'output_directory') + 'Book.djvu', 'DjVu Document (*.djvu)')
    
    if str(self.outFile) != '':
      self.projectFilesUi.outputFile.setText(self.outFile)
      self.config.set('startup', 'output_directory', os.path.split(str(self.outFile))[0] + '/')

  
  def addToProject(self):
    for item in self.projectFilesUi.offProjectList.selectedItems():
      self.projectFilesUi.offProjectList.takeItem(self.projectFilesUi.offProjectList.row(item))
      self.projectFilesUi.inProjectList.addItem(item)


  
  def removeFromProject(self):
    for item in self.projectFilesUi.inProjectList.selectedItems():
      self.projectFilesUi.inProjectList.takeItem(self.projectFilesUi.inProjectList.row(item))
      self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def projectFilesAccepted(self):
    if self.projectFilesUi.inProjectList.count() == 0:
      QMessageBox.warning(self, 'Warning', 'There are no pages to process.\nPlease add them using the green arrows.', QMessageBox.Ok, QMessageBox.Ok)
    elif str(self.projectFilesUi.outputFile.text()) == '':
      QMessageBox.warning(self, 'Warning', 'No output file has been selected.\nPlease select one using the "Output File" form.', QMessageBox.Ok, QMessageBox.Ok)
    else:
      self.projectFiles.close()
      
      for i in range(self.projectFilesUi.inProjectList.count()):
        orig = self.projectFilesUi.inProjectList.item(i)
        item = BookListWidgetItem(str(orig.text()), str(orig.statusTip()))
        
        if orig.text() not in [str(self.ui.pageList.item(i).text()) for i in range(self.ui.pageList.count())]:
          self.ui.pageList.addItem(item)
      
      self.hideBackground()
      self.thumbnailer.start()
      self.ui.startButton.setEnabled(True)
  
  
  
  def removeItems(self):
    for item in self.ui.pageList.selectedItems():
      self.ui.pageList.takeItem(self.ui.pageList.row(item))
    
    self.hideBackground()
  
  
  
  def debug(self, message):  self.ui.debugLog.add(message)
  
  
  
  def togglePreviews(self, on = True):
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
  
  
  
  def finishedBinding(self):
    self.ui.progressBar.reset()
    
    self.ui.startButton.setText('Start')
    self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
    
    
    if pynotify:
      notification = pynotify.Notification('Bindery', 'Your book has finished binding', '/opt/bindery/icons/logo.png')
      notification.show()
    else:
      QMessageBox.information(self, 'Message', 'The book has been succesfully saved!', QMessageBox.Ok, QMessageBox.Ok)
    
    for i in range(self.ui.pageList.count()):
      self.ui.pageList.item(i).setBackground(QColor(0, 0, 0, 0))
  
  
  def startBinding(self):
    if str(self.ui.startButton.text()) == 'Start':
      self.pages = [self.ui.pageList.item(i) for i in range(self.ui.pageList.count())]
    
      self.ui.startButton.setText('Stop')
      self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-stop', QIcon(':/icons/media-playback-stop.png')))
      
      
      self.options = {'cores':             -1,
                      'ocr':               (self.ui.enableOCR.checkState() != 0),
                      'ocr_engine':        str(self.ui.ocrEngine.currentText()).lower(),
                      'output_format':     str(self.ui.outputFormat.currentText()).lower(),
                      'cuneiform_options': str(self.ui.ocrOptions.text()),
                      'tesseract_options': str(self.ui.ocrOptions.text()),
                      'bitonal_encoder':   str(self.ui.bitonalEncoder.currentText()),
                      'color_encoder':     str(self.ui.colorEncoder.currentText()),
                      'c44_options':       str(self.ui.c44Options.text()),
                      'cjb2_options':      str(self.ui.cjb2Options.text()),
                      'cpaldjvu_options':  str(self.ui.cpaldjvuOptions.text()),
                      'csepdjvu_options':  str(self.ui.csepdjvuOptions.text()),
                      'minidjvu_options':  str(self.ui.minidjvuOptions.text()),
                      'numbering_type':    [],
                      'numbering_start':   [],
                      'win_path':          'C:\\Program Files\\DjVuZone\\DjVuLibre\\'}
      
      self.binder.initialize(self.pages, self.options, self.outFile)
      self.binder.start()
    else:
      self.binder.die = True
      self.ui.progressBar.reset()
      
      self.ui.startButton.setText('Start')
      self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
