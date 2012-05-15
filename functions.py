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



class Bindery(QMainWindow):
  def notImplemented(self):
    QMessageBox.information(self, 'Bindery', 'This feature is still being implemented.', QMessageBox.Ok, QMessageBox.Ok)



  def aboutBindery(self):
    QMessageBox.about(self, 'About ' + self.full_name, '''
    <h1>{}</h1>

    <h2>Description</h2>
    <p>
      {}
    </p>

    <h2>Modules</h2>
    <p>
      Bindery bundles a modified version <a href="http://code.google.com/p/djvubind/">djvubind</a>, a command-line DjVu
      document binder written in Python. Without this project, Bindery would never have started. I would like to thank
      strider1551 for his wonderful project!
    </p>

    <h2>Bugs and Feature Requests</h2>
    <p>
      If you find a bug in Bindery or would like to see a new feature added, please
      <a href="https://github.com/Blender3D/Bindery/issues">file a report</a> on GitHub. It's a painless process and helps keep all
      issues organized.
    </p>

    <h2>Legal</h2>
    <p>
      This software and all of its modules are licensed under the <a href="http://www.gnu.org/licenses/gpl.html">GNU Public License</a>.
    </p>

    <p>
      <small>
        Copyright &copy; 2012 Blender3D  &lt;<a href="mailto:"></a>&gt;
      </small>
    </p>
    '''.format(self.full_name, self.description))



  def aboutQt(self):
    QMessageBox.aboutQt(self)



  def checkDependencies(self):
    ocr_engines = [str(self.ui.ocrEngine.itemText(index)) for index in range(self.ui.ocrEngine.count())]
    installed_ocr_engines = []
    
    if not utils.is_executable('identify'):
      os.environ['path'] = os.path.abspath('bin/') + ';' + os.environ['path']
    
    for index, engine in enumerate(ocr_engines):
      if utils.is_executable(engine.lower()):
        installed_ocr_engines.append(engine)
      else:
        self.ui.ocrEngine.removeItem(index)

    if not installed_ocr_engines:
      self.ui.ocrTab.setEnabled(False)
    
    if not utils.is_executable('pdfbeads'):
      self.ui.outputFormat.model().itemFromIndex(self.ui.outputFormat.model().index(1, self.ui.outputFormat.modelColumn(), self.ui.outputFormat.rootModelIndex())).setEnabled(False)



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
        widget.setEnabled(len(self.selected) > 0)

      self.ui.singlePageFrame.setEnabled(len(self.selected) == 1)

      if len(self.selected) == 1:
        row = self.ui.pageList.row(self.selected[0])

        self.ui.moveToTopButton.setEnabled(row != 0)
        self.ui.moveUpButton.setEnabled(row != 0)

        self.ui.moveToBottomButton.setEnabled(row != self.ui.pageList.count() - 1)
        self.ui.moveDownButton.setEnabled(row != self.ui.pageList.count() - 1)

        self.previewer.image = self.selected[0].path
        self.previewer.size = [self.ui.pagePreview.size().width(), self.ui.pagePreview.size().width()]
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
    for item in self.projectFiles.ui.offProjectList.selectedItems():
      self.projectFiles.ui.offProjectList.takeItem(self.projectFiles.ui.offProjectList.row(item))
      self.projectFiles.ui.inProjectList.addItem(item)



  def removeFromProject(self):
    for item in self.projectFiles.ui.inProjectList.selectedItems():
      self.projectFiles.ui.inProjectList.takeItem(self.projectFiles.ui.inProjectList.row(item))
      self.projectFiles.ui.offProjectList.addItem(item)


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
    self.ui.outputFile.setText(self.projectFiles.ui.outputFile.text())

    if self.projectFiles.ui.inProjectList.count() == 0:
      QMessageBox.warning(self, 'Bindery', 'There are no pages to process.\nPlease add them using the arrows.', QMessageBox.Ok, QMessageBox.Ok)
    elif self.ui.outputFile.text() == '':
      QMessageBox.warning(self, 'Bindery', 'No output file has been selected.\nPlease select one using the "Output File" form.', QMessageBox.Ok, QMessageBox.Ok)
    else:
      self.projectFiles.close()

      for i in range(self.projectFiles.ui.inProjectList.count()):
        orig = self.projectFiles.ui.inProjectList.item(i)
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


  def reloadThumbnails(self):
    self.thumbnailer.die = False
    self.thumbnailer.start()


  def togglePreviews(self):
    self.previews = not self.previews

    if not self.previews:
      self.ui.actionReload_Thumbnails.setEnabled(False)

      self.thumbnailer.die = True

      while self.thumbnailer.isRunning():
        time.wait(0.1)

      for i in range(self.ui.pageList.count()):
        self.ui.pageList.item(i).removeIcon()

      self.thumbnailer.start()
    else:
      for i in range(self.ui.pageList.count()):
        self.ui.pageList.item(i).setSizeHint(QSize(72, 72))
        self.ui.pageList.item(i).resetIcon()

      self.ui.actionReload_Thumbnails.setEnabled(True)
      self.reloadThumbnails()



  def updateProgress(self, value, message):
    self.ui.progressBar.setValue(value)
    self.ui.progressBar.setFormat('{0} - %p%'.format(message))



  def updateBackground(self, item, color):
    self.ui.pageList.item(item).setBackground(color)



  def clearDebugLog(self):
    if QMessageBox.question(self, 'Bindery', 'Are you sure you want to clear the debug log?', QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
      self.ui.debugLog.clear()



  def finishedBinding(self):
    self.ui.progressBar.reset()

    self.ui.startButton.setText('Start')
    self.ui.startButton.setIcon(self.QIconFromTheme('media-playback-start'))
    self.ui.startBindingMenuItem.setIcon(self.QIconFromTheme('media-playback-start'))

    if notify:
      notification = pynotify.Notification('Bindery', 'Your book has finished binding', os.path.abspath('ui/icons/logo.png'))
      notification.show()
    else:
      QMessageBox.information(self, 'Bindery', 'Your book has finished binding.', QMessageBox.Ok, QMessageBox.Ok)

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
        'keywords':          str(self.ui.bookKeywords.text())
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
