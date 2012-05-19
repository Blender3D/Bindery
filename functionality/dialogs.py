import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dialogs(QMainWindow):
  def error(self, message):
    QMessageBox.critical(self, '', message, QMessageBox.Ok, QMessageBox.Ok)

    if self.binder.isRunning():
      self.binder.stop()
  
  
  
  def showFileDialog(self):
    directory = str(QFileDialog.getExistingDirectory(
      self,
      'Input directory',
      self.settings.value('startup/input_directory', QDir.homePath()).toString()
    ))

    if directory:
      directory = os.path.abspath(directory)
      self.projectFiles.ui.inputDirectory.setText(directory)
      
      self.settings.setValue('startup/input_directory', directory)

      for filename in os.listdir(directory):
        item = QListWidgetItem(os.path.split(filename)[-1])
        item.setStatusTip(os.path.join(directory, filename))
        
        if os.path.splitext(os.path.split(filename)[-1])[-1].lower() not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
          item.setFlags(Qt.NoItemFlags)

        self.projectFiles.ui.offProjectList.addItem(item)
  
  
  
  def showSaveDialog(self):
    extension = str(self.ui.outputFormat.currentText())
    filename = 'Book.{extension}'.format(extension=extension.lower())
    filetype = '{filetype} Document (*.{extension})'.format(filetype=extension, extension=extension.lower())
    
    dialog = QFileDialog.getSaveFileName(
      self,
      'Save output file',
      os.path.join(str(self.settings.value('startup/output_directory', QDir.homePath()).toString()), filename),
      filetype
    )

    if dialog:
      self.ui.outputFile.setText(dialog)
      
      if str(self.ui.outputFile.text()) != '':
        self.projectFiles.ui.outputFile.setText(self.ui.outputFile.text())
        self.settings.setValue('startup/output_directory', os.path.split(str(self.ui.outputFile.text()))[0] + '/')

        return dialog
    else:
      return False
  
  
  
  def showProjectDialog(self):
    self.projectFiles.show()
  
  
  
  def addFiles(self):
    for filename in QFileDialog.getOpenFileNames(
      self,
      'Add files to project',
      self.settings.value('startup/input_directory', QDir.homePath()).toString()
    ):
      self.addFile(filename)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
  
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      
      self.thumbnailer.start()
  
  
  
  def saveDebugLog(self):
    output = QFileDialog.getSaveFileName(self, 'Save debug log', 'bindery.log', 'Log File (*.log)')
    
    if output:
      handle = open(output, 'w')
      handle.write(self.ui.debugLog.plainText())
      handle.close()
