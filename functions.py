import sys, os, time, glob

import config

from BookListWidget import * 
from thumbnailer import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
  import pynotify
  pynotify.init('Bindery')
  
  notify = True
except:
  notify = False

class StartQT4(QMainWindow):
  def error(self, message):
    QMessageBox.critical(self, '', message, QMessageBox.Ok, QMessageBox.Ok)
    self.toggleBinding()
  
  
  
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
    
    for widget in [self.ui.removePageButton, self.ui.removePageMenuItem]:
      widget.setEnabled(len(self.selected) > 0)
    
    self.ui.pageTab.setEnabled(len(self.selected) == 1)
    
    if len(self.selected) == 1:
      row = self.ui.pageList.row(self.selected[0])
      
      self.ui.moveToTopButton.setEnabled(row != 0)
      self.ui.moveUpButton.setEnabled(row != 0)
      
      self.ui.moveToBottomButton.setEnabled(row != self.ui.pageList.count() - 1)
      self.ui.moveDownButton.setEnabled(row != self.ui.pageList.count() - 1)
      
      self.previewer.image = self.selected[0].filepath
      self.previewer.size = [self.ui.pagePreview.size().width() * 2, self.ui.pagePreview.size().width() * 2]
      self.previewer.start()
  
  
  
  def moveItemToTop(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(0, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(0)
  
  
  
  def moveItemUp(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(currentRow - 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(currentRow - 1 if currentRow != 0 else 0)
  
  
  
  def moveItemDown(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(currentRow + 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(currentRow + 1 if currentRow != self.ui.pageList.count() - 1 else self.ui.pageList.count() - 1) 
  
  
  def moveItemToBottom(self):
    currentRow = self.ui.pageList.row(self.ui.pageList.currentItem())
    
    self.ui.pageList.insertItem(self.ui.pageList.count() - 1, self.ui.pageList.takeItem(currentRow))
    self.ui.pageList.setCurrentRow(self.ui.pageList.count() - 1)
  
  
  
  def pageGrayscaleChanged(self, state):
    self.ui.pageList.selectedItems()[0].grayscale = (state == 2)
  
  
  
  def makeIcon(self, index, icon):
    item = self.ui.pageList.item(index)
    item.setIcon(QIcon(QPixmap.fromImage(icon)))
  
  
  
  def outputFormatChanged(self, choice):
    self.ui.stackedWidget.setCurrentIndex(choice)
  
  
  def hideBackground(self):
    if self.ui.pageList.count() > 0:
      self.ui.pageList.setStyleSheet('')
    else:
      self.ui.pageList.setStyleSheet('''QListWidget {
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
                                        }''')
  

  
  def showProjectDialog(self):  self.projectFiles.show()    



  def showFileDialog(self):
    directory = QFileDialog.getExistingDirectory(self, 'Input directory', self.config.get('startup', 'input_directory'))
    
    if str(directory) != '':
      self.projectFilesUi.inputDirectory.setText(str(directory) + '/')
      
      self.config.set('startup', 'input_directory', str(directory) + '/')
      
      for file in glob.glob(str(directory) + '/*'):
        item = QListWidgetItem(os.path.split(file)[-1])
        item.setStatusTip(file)
        
        if os.path.splitext(os.path.split(file)[-1])[-1] not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
          item.setFlags(Qt.NoItemFlags)
        
        self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def showSaveDialog(self):
    file = str(self.ui.outputFormat.currentText())
    filename = 'Book.{0}'.format(file.lower())
    filetype = '{0} Document (*.{1})'.format(file, file.lower())
    
    self.ui.outputFile.setText(QFileDialog.getSaveFileName(self, 'Save output file', self.config.get('startup', 'output_directory') + filename, filetype))
    
    if str(self.ui.outputFile.text()) != '':
      self.projectFilesUi.outputFile.setText(self.ui.outputFile.text())
      self.config.set('startup', 'output_directory', os.path.split(str(self.ui.outputFile.text()))[0] + '/')

  
  def addToProject(self):
    for item in self.projectFilesUi.offProjectList.selectedItems():
      self.projectFilesUi.offProjectList.takeItem(self.projectFilesUi.offProjectList.row(item))
      self.projectFilesUi.inProjectList.addItem(item)


  
  def removeFromProject(self):
    for item in self.projectFilesUi.inProjectList.selectedItems():
      self.projectFilesUi.inProjectList.takeItem(self.projectFilesUi.inProjectList.row(item))
      self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def filesDropped(self, files):
    for file in files:
      file = str(file)
      
      if os.path.splitext(os.path.split(file)[-1])[-1] in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
        item = BookListWidgetItem(os.path.split(file)[-1], file)
        
        if file not in [str(self.ui.pageList.item(i).filepath) for i in range(self.ui.pageList.count())]:
          self.ui.pageList.addItem(item)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
  
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      self.thumbnailer.start()
  
  
  
  def addFiles(self):
    for file in QFileDialog.getOpenFileNames(self, 'Add files to project', self.config.get('startup', 'input_directory')):
      file = str(file)

      if os.path.splitext(os.path.split(file)[-1])[-1] in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
        item = BookListWidgetItem(os.path.split(file)[-1], file)
        
        if file not in [str(self.ui.pageList.item(i).filepath) for i in range(self.ui.pageList.count())]:
          self.ui.pageList.addItem(item)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
  
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      self.thumbnailer.start()
  
  
  
  def changeOCRLanguage(self, language):
    currentOptions = str(self.ui.ocrOptions.text())
    arguments = currentOptions.split(' ')
    
    if currentOptions.find('-l') != -1:
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
    self.ui.startBindingMenuItem.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
    
    if notify:
      notification = pynotify.Notification('Bindery', 'Your book has finished binding', '/opt/bindery/source/ui/icons/logo.png')
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
      self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-stop', QIcon(':/icons/media-playback-stop.png')))
      self.ui.startBindingMenuItem.setIcon(QIcon.fromTheme('media-playback-stop', QIcon(':/icons/media-playback-stop.png')))
      
      self.options = {'ocr':               (self.ui.enableOCR.checkState() != 0),
                      'ocr_engine':        str(self.ui.ocrEngine.currentText()).lower(),
                      'output_format':     str(self.ui.outputFormat.currentText()).lower(),
                      'ocr_options':       str(self.ui.ocrOptions.text()),
                      'color_encoder':     str(self.ui.djvuColorEncoder.currentText()),
                      'c44_options':       str(self.ui.c44Options.text()),
                      'cjb2_options':      str(self.ui.cjb2Options.text()),
                      'cpaldjvu_options':  str(self.ui.cpaldjvuOptions.text()),
                      'csepdjvu_options':  str(self.ui.csepdjvuOptions.text()),
                      'minidjvu_options':  str(self.ui.minidjvuOptions.text()),
                      'numbering_type':    [],
                      'numbering_start':   [],
                      'win_path':          'C:\\Program Files\\DjVuZone\\DjVuLibre\\'}
      
     
      if self.options['output_format'] == 'djvu':
        self.options['bitonal_encoder'] = str(self.ui.djvuBitonalEncoder.currentText())
      elif self.options['output_format'] == 'pdf':
        self.options['bitonal_encoder'] = str(self.ui.pdfBitonalEncoder.currentText())
      
      
      self.binder.initialize(self.pages, self.options, str(self.ui.outputFile.text()))
      self.binder.start()
    else:
      self.binder.die = True
      self.ui.progressBar.reset()
      
      self.ui.startButton.setText('Start')
      self.ui.startButton.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
      self.ui.startBindingMenuItem.setIcon(QIcon.fromTheme('media-playback-start', QIcon(':/icons/media-playback-start.png')))
      
      for i in range(self.ui.pageList.count()):
        self.ui.pageList.item(i).setBackground(QColor(0, 0, 0, 0))
