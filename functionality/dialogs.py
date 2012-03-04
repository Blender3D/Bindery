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
      self.settings.value('startup/input_directory', QDir.homePath())
      ,asd
    )

    if str(directory) != '':
      self.projectFilesUi.inputDirectory.setText(str(directory) + '/')
      
      self.settings.setValue('startup/input_directory', str(directory) + '/')
      
      for file in glob.glob(str(directory) + '/*'):
        item = QListWidgetItem(os.path.split(file)[-1])
        item.setStatusTip(file)
        
        if os.path.splitext(os.path.split(file)[-1])[-1] not in ['.jpg', '.jpeg', '.bmp', '.png', '.tif', '.tiff']:
          item.setFlags(Qt.NoItemFlags)

        self.projectFilesUi.offProjectList.addItem(item)
  
  
  
  def showSaveDialog(self):
    extension = str(self.ui.outputFormat.currentText())
    filename = 'Book.{extension}'.format(extension=extension.lower())
    filetype = '{filetype} Document (*.{extension})'.format(filetype=extension, extension=extension.lower())
    
    self.ui.outputFile.setText(QFileDialog.getSaveFileName(
      self,
      'Save output file',
      os.path.join(self.settings.value('startup/output_directory', QDir.homePath()), filename), filetype)
    )
    
    if str(self.ui.outputFile.text()) != '':
      self.projectFilesUi.outputFile.setText(self.ui.outputFile.text())
      self.settings.setValue('startup/output_directory', os.path.split(str(self.ui.outputFile.text()))[0] + '/')
  
  
  
  def showProjectDialog(self):
    self.projectFiles.show()
  
  
  
  def addFiles(self):
    for filename in QFileDialog.getOpenFileNames(
      self,
      'Add files to project',
      self.settings.value('startup/input_directory', QDir.homePath())
    ):
      self.addFile(filename)
    
    for widget in [self.ui.startButton, self.ui.startBindingMenuItem]:
      widget.setEnabled(self.ui.pageList.count() > 0)
  
    if self.ui.pageList.count() > 0:
      self.hideBackground()
      
      self.thumbnailer.start()
  
  
  
  def saveDebugLog(self):
    output = QFileDialog.getSaveFileName(self, 'Save debug log', 'bindery.log', 'Log file (*.log)')
    
    if output:
      handle = open(output, 'w')
      table = []
      
      table.append(['Time', 'Caller', 'Message', 'Level'])
      
      for i in range(self.ui.debugLog.topLevelItemCount()):
        item = self.ui.debugLog.topLevelItem(i)
        table.append([str(item.text(j)) for j in range(item.columnCount())])
      
      column_paddings = []
      
      for i in range(len(table[0])):
        column_paddings.append(max([len(row[i]) for row in table]))

      for row in table:
        handle.write(row[0].ljust(column_paddings[0] + 4))

        for i in range(1, len(row)):
          handle.write(row[i].ljust(column_paddings[i] + 4))
        
        handle.write('\n')
