import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dialogs(QMainWindow):
  def error(self, message):
    QMessageBox.critical(self, '', message, QMessageBox.Ok, QMessageBox.Ok)
    self.toggleBinding()
  
  
  
  def showFileDialog(self):
    directory = QFileDialog.getExistingDirectory(
      self,
      'Input directory',
      self.settings.value('startup/input_directory', QDir.homePath()).toString()
    )

    if str(directory) != '':
      self.projectFilesUi.inputDirectory.setText(str(directory) + os.pathsep)
      
      self.settings.setValue('startup/input_directory', str(directory) + os.pathsep)
      
      for file in glob.glob(str(directory) + '/*'):
        item = QListWidgetItem(os.path.split(file)[-1])
        item.setStatusTip(file)
        
        if os.path.splitext(os.path.split(file)[-1])[-1].lower() not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
          item.setFlags(Qt.NoItemFlags)

        self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def showSaveDialog(self):
    extension = str(self.ui.outputFormat.currentText())
    filename = 'Book.{extension}'.format(extension=extension.lower())
    filetype = '{filetype} Document (*.{extension})'.format(filetype=extension, extension=extension.lower())
    
    self.ui.outputFile.setText(QFileDialog.getSaveFileName(
      self,
      'Save output file',
      os.path.join(str(self.settings.value('startup/output_directory', QDir.homePath()).toString()), filename),
      filetype
    ))
    
    if str(self.ui.outputFile.text()) != '':
      self.projectFilesUi.outputFile.setText(self.ui.outputFile.text())
      self.settings.setValue('startup/output_directory', os.path.split(str(self.ui.outputFile.text()))[0] + '/')
  
  
  
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
