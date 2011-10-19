# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/gui.ui'
#
# Created: Wed Oct 19 01:35:02 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName(_fromUtf8("MainWindow"))
    MainWindow.setEnabled(True)
    MainWindow.resize(749, 566)
    MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bindery", None, QtGui.QApplication.UnicodeUTF8))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)
    MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.splitter = QtGui.QSplitter(self.centralwidget)
    self.splitter.setOrientation(QtCore.Qt.Horizontal)
    self.splitter.setObjectName(_fromUtf8("splitter"))
    self.widget = QtGui.QWidget(self.splitter)
    self.widget.setObjectName(_fromUtf8("widget"))
    self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
    self.verticalLayout_3.setMargin(0)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.verticalLayout_2 = QtGui.QVBoxLayout()
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.label_8 = QtGui.QLabel(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
    self.label_8.setSizePolicy(sizePolicy)
    self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Add and arrange the book\'s pages below", None, QtGui.QApplication.UnicodeUTF8))
    self.label_8.setAlignment(QtCore.Qt.AlignCenter)
    self.label_8.setObjectName(_fromUtf8("label_8"))
    self.verticalLayout_2.addWidget(self.label_8)
    self.pageList = BookListWidget(self.widget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pageList.sizePolicy().hasHeightForWidth())
    self.pageList.setSizePolicy(sizePolicy)
    self.pageList.setStyleSheet(_fromUtf8("QListView\n"
"{\n"
"background-image: url(\":/icons/go-down-big.png\");\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"background-color: white;\n"
"}\n"
"\n"
"QListView:hover\n"
"{\n"
"background-image: url(\":/icons/go-down-big-hover.png\");\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"background-color: white;\n"
"}"))
    self.pageList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.pageList.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
    self.pageList.setUniformItemSizes(True)
    self.pageList.setObjectName(_fromUtf8("pageList"))
    self.verticalLayout_2.addWidget(self.pageList)
    self.verticalLayout_3.addLayout(self.verticalLayout_2)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.addPageButton = QtGui.QPushButton(self.widget)
    self.addPageButton.setText(QtGui.QApplication.translate("MainWindow", "Add page", None, QtGui.QApplication.UnicodeUTF8))
    self.addPageButton.setObjectName(_fromUtf8("addPageButton"))
    self.horizontalLayout.addWidget(self.addPageButton)
    spacerItem = QtGui.QSpacerItem(50, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem)
    self.removePageButton = QtGui.QPushButton(self.widget)
    self.removePageButton.setEnabled(False)
    self.removePageButton.setText(QtGui.QApplication.translate("MainWindow", "Remove page", None, QtGui.QApplication.UnicodeUTF8))
    self.removePageButton.setAutoRepeat(False)
    self.removePageButton.setFlat(False)
    self.removePageButton.setObjectName(_fromUtf8("removePageButton"))
    self.horizontalLayout.addWidget(self.removePageButton)
    self.verticalLayout_3.addLayout(self.horizontalLayout)
    self.layoutWidget = QtGui.QWidget(self.splitter)
    self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
    self.verticalLayout.setMargin(0)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.tabWidget = QtGui.QTabWidget(self.layoutWidget)
    self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
    self.tabWidget.setMovable(True)
    self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
    self.tab = QtGui.QWidget()
    self.tab.setEnabled(False)
    self.tab.setObjectName(_fromUtf8("tab"))
    self.gridLayout = QtGui.QGridLayout(self.tab)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.verticalLayout1 = QtGui.QVBoxLayout()
    self.verticalLayout1.setObjectName(_fromUtf8("verticalLayout1"))
    self.graphicsView = QtGui.QGraphicsView(self.tab)
    self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
    self.verticalLayout1.addWidget(self.graphicsView)
    self.horizontalLayout1 = QtGui.QHBoxLayout()
    self.horizontalLayout1.setObjectName(_fromUtf8("horizontalLayout1"))
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout1.addItem(spacerItem1)
    self.moveToTopButton = QtGui.QToolButton(self.tab)
    self.moveToTopButton.setEnabled(False)
    self.moveToTopButton.setText(QtGui.QApplication.translate("MainWindow", "Very Top", None, QtGui.QApplication.UnicodeUTF8))
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-top.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.moveToTopButton.setIcon(icon1)
    self.moveToTopButton.setIconSize(QtCore.QSize(32, 32))
    self.moveToTopButton.setObjectName(_fromUtf8("moveToTopButton"))
    self.horizontalLayout1.addWidget(self.moveToTopButton)
    self.moveUpButton = QtGui.QToolButton(self.tab)
    self.moveUpButton.setEnabled(False)
    self.moveUpButton.setText(QtGui.QApplication.translate("MainWindow", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.moveUpButton.setIcon(icon2)
    self.moveUpButton.setIconSize(QtCore.QSize(32, 32))
    self.moveUpButton.setObjectName(_fromUtf8("moveUpButton"))
    self.horizontalLayout1.addWidget(self.moveUpButton)
    self.moveDownButton = QtGui.QToolButton(self.tab)
    self.moveDownButton.setEnabled(False)
    self.moveDownButton.setText(QtGui.QApplication.translate("MainWindow", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.moveDownButton.setIcon(icon3)
    self.moveDownButton.setIconSize(QtCore.QSize(32, 32))
    self.moveDownButton.setObjectName(_fromUtf8("moveDownButton"))
    self.horizontalLayout1.addWidget(self.moveDownButton)
    self.moveToBottomButton = QtGui.QToolButton(self.tab)
    self.moveToBottomButton.setEnabled(False)
    self.moveToBottomButton.setText(QtGui.QApplication.translate("MainWindow", "Very Bottom", None, QtGui.QApplication.UnicodeUTF8))
    icon4 = QtGui.QIcon()
    icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-bottom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.moveToBottomButton.setIcon(icon4)
    self.moveToBottomButton.setIconSize(QtCore.QSize(32, 32))
    self.moveToBottomButton.setObjectName(_fromUtf8("moveToBottomButton"))
    self.horizontalLayout1.addWidget(self.moveToBottomButton)
    spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout1.addItem(spacerItem2)
    self.verticalLayout1.addLayout(self.horizontalLayout1)
    self.gridLayout.addLayout(self.verticalLayout1, 0, 0, 1, 1)
    spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
    self.pageGrayscale = QtGui.QCheckBox(self.tab)
    self.pageGrayscale.setEnabled(False)
    self.pageGrayscale.setText(QtGui.QApplication.translate("MainWindow", "Grayscale", None, QtGui.QApplication.UnicodeUTF8))
    self.pageGrayscale.setObjectName(_fromUtf8("pageGrayscale"))
    self.gridLayout.addWidget(self.pageGrayscale, 2, 0, 1, 1)
    self.tabWidget.addTab(self.tab, _fromUtf8(""))
    self.tab2 = QtGui.QWidget()
    self.tab2.setObjectName(_fromUtf8("tab2"))
    self.formLayout0 = QtGui.QFormLayout(self.tab2)
    self.formLayout0.setObjectName(_fromUtf8("formLayout0"))
    self.outputFormatLabel = QtGui.QLabel(self.tab2)
    self.outputFormatLabel.setText(QtGui.QApplication.translate("MainWindow", "Output Format", None, QtGui.QApplication.UnicodeUTF8))
    self.outputFormatLabel.setObjectName(_fromUtf8("outputFormatLabel"))
    self.formLayout0.setWidget(0, QtGui.QFormLayout.FieldRole, self.outputFormatLabel)
    self.outputFormat = QtGui.QComboBox(self.tab2)
    self.outputFormat.setMaximumSize(QtCore.QSize(100, 16777215))
    self.outputFormat.setObjectName(_fromUtf8("outputFormat"))
    self.outputFormat.addItem(_fromUtf8(""))
    self.outputFormat.setItemText(0, QtGui.QApplication.translate("MainWindow", "DjVu", None, QtGui.QApplication.UnicodeUTF8))
    self.outputFormat.addItem(_fromUtf8(""))
    self.outputFormat.setItemText(1, QtGui.QApplication.translate("MainWindow", "PDF", None, QtGui.QApplication.UnicodeUTF8))
    self.outputFormat.addItem(_fromUtf8(""))
    self.outputFormat.setItemText(2, QtGui.QApplication.translate("MainWindow", "PostScript", None, QtGui.QApplication.UnicodeUTF8))
    self.formLayout0.setWidget(0, QtGui.QFormLayout.LabelRole, self.outputFormat)
    self.tabWidget.addTab(self.tab2, _fromUtf8(""))
    self.tab3 = QtGui.QWidget()
    self.tab3.setObjectName(_fromUtf8("tab3"))
    self.formLayout1 = QtGui.QFormLayout(self.tab3)
    self.formLayout1.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
    self.formLayout1.setObjectName(_fromUtf8("formLayout1"))
    self.enableOCR = QtGui.QCheckBox(self.tab3)
    self.enableOCR.setText(QtGui.QApplication.translate("MainWindow", "Enable OCR", None, QtGui.QApplication.UnicodeUTF8))
    self.enableOCR.setObjectName(_fromUtf8("enableOCR"))
    self.formLayout1.setWidget(0, QtGui.QFormLayout.SpanningRole, self.enableOCR)
    self.ocrEngine = QtGui.QComboBox(self.tab3)
    self.ocrEngine.setEnabled(False)
    self.ocrEngine.setObjectName(_fromUtf8("ocrEngine"))
    self.ocrEngine.addItem(_fromUtf8(""))
    self.ocrEngine.setItemText(0, QtGui.QApplication.translate("MainWindow", "Tesseract", None, QtGui.QApplication.UnicodeUTF8))
    self.ocrEngine.addItem(_fromUtf8(""))
    self.ocrEngine.setItemText(1, QtGui.QApplication.translate("MainWindow", "Cuniform", None, QtGui.QApplication.UnicodeUTF8))
    self.formLayout1.setWidget(1, QtGui.QFormLayout.LabelRole, self.ocrEngine)
    self.ocrEngineLabel = QtGui.QLabel(self.tab3)
    self.ocrEngineLabel.setText(QtGui.QApplication.translate("MainWindow", "OCR Engine", None, QtGui.QApplication.UnicodeUTF8))
    self.ocrEngineLabel.setObjectName(_fromUtf8("ocrEngineLabel"))
    self.formLayout1.setWidget(1, QtGui.QFormLayout.FieldRole, self.ocrEngineLabel)
    self.ocrOptions = QtGui.QLineEdit(self.tab3)
    self.ocrOptions.setEnabled(False)
    self.ocrOptions.setLayoutDirection(QtCore.Qt.LeftToRight)
    self.ocrOptions.setObjectName(_fromUtf8("ocrOptions"))
    self.formLayout1.setWidget(2, QtGui.QFormLayout.LabelRole, self.ocrOptions)
    self.ocrOptionsLabel = QtGui.QLabel(self.tab3)
    self.ocrOptionsLabel.setEnabled(True)
    self.ocrOptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "Engine Options", None, QtGui.QApplication.UnicodeUTF8))
    self.ocrOptionsLabel.setObjectName(_fromUtf8("ocrOptionsLabel"))
    self.formLayout1.setWidget(2, QtGui.QFormLayout.FieldRole, self.ocrOptionsLabel)
    self.tabWidget.addTab(self.tab3, _fromUtf8(""))
    self.widget1 = QtGui.QWidget()
    self.widget1.setObjectName(_fromUtf8("widget1"))
    self.formLayout = QtGui.QFormLayout(self.widget1)
    self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
    self.formLayout.setObjectName(_fromUtf8("formLayout"))
    self.bitonalEncoderLabel = QtGui.QLabel(self.widget1)
    self.bitonalEncoderLabel.setText(QtGui.QApplication.translate("MainWindow", "Bitonal Encoder", None, QtGui.QApplication.UnicodeUTF8))
    self.bitonalEncoderLabel.setObjectName(_fromUtf8("bitonalEncoderLabel"))
    self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.bitonalEncoderLabel)
    self.bitonalEncoder = QtGui.QComboBox(self.widget1)
    self.bitonalEncoder.setObjectName(_fromUtf8("bitonalEncoder"))
    self.bitonalEncoder.addItem(_fromUtf8(""))
    self.bitonalEncoder.setItemText(0, QtGui.QApplication.translate("MainWindow", "minidjvu", None, QtGui.QApplication.UnicodeUTF8))
    self.bitonalEncoder.addItem(_fromUtf8(""))
    self.bitonalEncoder.setItemText(1, QtGui.QApplication.translate("MainWindow", "cjb2", None, QtGui.QApplication.UnicodeUTF8))
    self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.bitonalEncoder)
    self.colorEncoderLabel = QtGui.QLabel(self.widget1)
    self.colorEncoderLabel.setText(QtGui.QApplication.translate("MainWindow", "Color Encoder", None, QtGui.QApplication.UnicodeUTF8))
    self.colorEncoderLabel.setObjectName(_fromUtf8("colorEncoderLabel"))
    self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.colorEncoderLabel)
    self.colorEncoder = QtGui.QComboBox(self.widget1)
    self.colorEncoder.setObjectName(_fromUtf8("colorEncoder"))
    self.colorEncoder.addItem(_fromUtf8(""))
    self.colorEncoder.setItemText(0, QtGui.QApplication.translate("MainWindow", "csepdjvu", None, QtGui.QApplication.UnicodeUTF8))
    self.colorEncoder.addItem(_fromUtf8(""))
    self.colorEncoder.setItemText(1, QtGui.QApplication.translate("MainWindow", "c44", None, QtGui.QApplication.UnicodeUTF8))
    self.colorEncoder.addItem(_fromUtf8(""))
    self.colorEncoder.setItemText(2, QtGui.QApplication.translate("MainWindow", "cpaldjvu", None, QtGui.QApplication.UnicodeUTF8))
    self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.colorEncoder)
    self.c44OptionsLabel = QtGui.QLabel(self.widget1)
    self.c44OptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "c44 Options", None, QtGui.QApplication.UnicodeUTF8))
    self.c44OptionsLabel.setObjectName(_fromUtf8("c44OptionsLabel"))
    self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.c44OptionsLabel)
    self.c44Options = QtGui.QLineEdit(self.widget1)
    self.c44Options.setObjectName(_fromUtf8("c44Options"))
    self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.c44Options)
    self.cjb2OptionsLabel = QtGui.QLabel(self.widget1)
    self.cjb2OptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "cjb2 Options", None, QtGui.QApplication.UnicodeUTF8))
    self.cjb2OptionsLabel.setObjectName(_fromUtf8("cjb2OptionsLabel"))
    self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.cjb2OptionsLabel)
    self.cjb2Options = QtGui.QLineEdit(self.widget1)
    self.cjb2Options.setText(QtGui.QApplication.translate("MainWindow", "-lossy", None, QtGui.QApplication.UnicodeUTF8))
    self.cjb2Options.setObjectName(_fromUtf8("cjb2Options"))
    self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cjb2Options)
    self.cpaldjvuOptionsLabel = QtGui.QLabel(self.widget1)
    self.cpaldjvuOptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "cpaldjvu Options", None, QtGui.QApplication.UnicodeUTF8))
    self.cpaldjvuOptionsLabel.setObjectName(_fromUtf8("cpaldjvuOptionsLabel"))
    self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.cpaldjvuOptionsLabel)
    self.cpaldjvuOptions = QtGui.QLineEdit(self.widget1)
    self.cpaldjvuOptions.setObjectName(_fromUtf8("cpaldjvuOptions"))
    self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cpaldjvuOptions)
    self.csepdjvuOptionsLabel = QtGui.QLabel(self.widget1)
    self.csepdjvuOptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "csepdjvu Options", None, QtGui.QApplication.UnicodeUTF8))
    self.csepdjvuOptionsLabel.setObjectName(_fromUtf8("csepdjvuOptionsLabel"))
    self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.csepdjvuOptionsLabel)
    self.csepdjvuOptions = QtGui.QLineEdit(self.widget1)
    self.csepdjvuOptions.setObjectName(_fromUtf8("csepdjvuOptions"))
    self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.csepdjvuOptions)
    self.minidjvuOptionsLabel = QtGui.QLabel(self.widget1)
    self.minidjvuOptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "minidjvu Options", None, QtGui.QApplication.UnicodeUTF8))
    self.minidjvuOptionsLabel.setObjectName(_fromUtf8("minidjvuOptionsLabel"))
    self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.minidjvuOptionsLabel)
    self.minidjvuOptions = QtGui.QLineEdit(self.widget1)
    self.minidjvuOptions.setText(QtGui.QApplication.translate("MainWindow", "--match -pages-per-dict 100", None, QtGui.QApplication.UnicodeUTF8))
    self.minidjvuOptions.setCursorPosition(27)
    self.minidjvuOptions.setObjectName(_fromUtf8("minidjvuOptions"))
    self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.minidjvuOptions)
    self.tabWidget.addTab(self.widget1, _fromUtf8(""))
    self.tab1 = QtGui.QWidget()
    self.tab1.setObjectName(_fromUtf8("tab1"))
    self.gridLayout_7 = QtGui.QGridLayout(self.tab1)
    self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
    self.verticalLayout1 = QtGui.QVBoxLayout()
    self.verticalLayout1.setObjectName(_fromUtf8("verticalLayout1"))
    self.debugLog = DebugLog(self.tab1)
    font = QtGui.QFont()
    font.setFamily(_fromUtf8("Monospace"))
    self.debugLog.setFont(font)
    self.debugLog.setLineWrapMode(QtGui.QTextEdit.NoWrap)
    self.debugLog.setReadOnly(True)
    self.debugLog.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Monospace\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
    self.debugLog.setObjectName(_fromUtf8("debugLog"))
    self.verticalLayout1.addWidget(self.debugLog)
    self.gridLayout_7.addLayout(self.verticalLayout1, 0, 0, 1, 1)
    self.tabWidget.addTab(self.tab1, _fromUtf8(""))
    self.verticalLayout.addWidget(self.tabWidget)
    self.horizontalLayout_7 = QtGui.QHBoxLayout()
    self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
    self.progressBar = QtGui.QProgressBar(self.layoutWidget)
    self.progressBar.setFormat(QtGui.QApplication.translate("MainWindow", "%p%", None, QtGui.QApplication.UnicodeUTF8))
    self.progressBar.setObjectName(_fromUtf8("progressBar"))
    self.horizontalLayout_7.addWidget(self.progressBar)
    self.startButton = QtGui.QPushButton(self.layoutWidget)
    self.startButton.setEnabled(False)
    self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
    self.startButton.setObjectName(_fromUtf8("startButton"))
    self.horizontalLayout_7.addWidget(self.startButton)
    self.verticalLayout.addLayout(self.horizontalLayout_7)
    self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
    MainWindow.setCentralWidget(self.centralwidget)
    self.menuBar = QtGui.QMenuBar(MainWindow)
    self.menuBar.setGeometry(QtCore.QRect(0, 0, 749, 25))
    self.menuBar.setObjectName(_fromUtf8("menuBar"))
    self.menuFile = QtGui.QMenu(self.menuBar)
    self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
    self.menuFile.setObjectName(_fromUtf8("menuFile"))
    self.menuEdit = QtGui.QMenu(self.menuBar)
    self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
    self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
    self.menuAbout = QtGui.QMenu(self.menuBar)
    self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
    self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
    self.menuView = QtGui.QMenu(self.menuBar)
    self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
    self.menuView.setObjectName(_fromUtf8("menuView"))
    self.menuPage_Style = QtGui.QMenu(self.menuView)
    self.menuPage_Style.setTitle(QtGui.QApplication.translate("MainWindow", "Page Style", None, QtGui.QApplication.UnicodeUTF8))
    self.menuPage_Style.setObjectName(_fromUtf8("menuPage_Style"))
    self.menuPage = QtGui.QMenu(self.menuBar)
    self.menuPage.setTitle(QtGui.QApplication.translate("MainWindow", "Page", None, QtGui.QApplication.UnicodeUTF8))
    self.menuPage.setObjectName(_fromUtf8("menuPage"))
    MainWindow.setMenuBar(self.menuBar)
    self.toolBar = QtGui.QToolBar(MainWindow)
    self.toolBar.setMovable(False)
    self.toolBar.setObjectName(_fromUtf8("toolBar"))
    MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
    self.newMenuItem = QtGui.QAction(MainWindow)
    self.newMenuItem.setText(QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
    self.newMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
    self.newMenuItem.setObjectName(_fromUtf8("newMenuItem"))
    self.openMenuItem = QtGui.QAction(MainWindow)
    self.openMenuItem.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
    self.openMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
    self.openMenuItem.setObjectName(_fromUtf8("openMenuItem"))
    self.saveMenuItem = QtGui.QAction(MainWindow)
    self.saveMenuItem.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
    self.saveMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
    self.saveMenuItem.setObjectName(_fromUtf8("saveMenuItem"))
    self.saveAsMenuItem = QtGui.QAction(MainWindow)
    self.saveAsMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Save &As...", None, QtGui.QApplication.UnicodeUTF8))
    self.saveAsMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+S", None, QtGui.QApplication.UnicodeUTF8))
    self.saveAsMenuItem.setObjectName(_fromUtf8("saveAsMenuItem"))
    self.quitMenuItem = QtGui.QAction(MainWindow)
    self.quitMenuItem.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
    self.quitMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
    self.quitMenuItem.setMenuRole(QtGui.QAction.QuitRole)
    self.quitMenuItem.setObjectName(_fromUtf8("quitMenuItem"))
    self.helpMenuItem = QtGui.QAction(MainWindow)
    self.helpMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
    self.helpMenuItem.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
    self.helpMenuItem.setObjectName(_fromUtf8("helpMenuItem"))
    self.aboutMenuItem = QtGui.QAction(MainWindow)
    self.aboutMenuItem.setText(QtGui.QApplication.translate("MainWindow", "About Bindery", None, QtGui.QApplication.UnicodeUTF8))
    self.aboutMenuItem.setObjectName(_fromUtf8("aboutMenuItem"))
    self.filePreviewsMenuItem = QtGui.QAction(MainWindow)
    self.filePreviewsMenuItem.setCheckable(True)
    self.filePreviewsMenuItem.setChecked(True)
    self.filePreviewsMenuItem.setText(QtGui.QApplication.translate("MainWindow", "File Previews", None, QtGui.QApplication.UnicodeUTF8))
    self.filePreviewsMenuItem.setObjectName(_fromUtf8("filePreviewsMenuItem"))
    self.advancedOptionsMenuItem = QtGui.QAction(MainWindow)
    self.advancedOptionsMenuItem.setCheckable(True)
    self.advancedOptionsMenuItem.setChecked(True)
    self.advancedOptionsMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Advanced Options", None, QtGui.QApplication.UnicodeUTF8))
    self.advancedOptionsMenuItem.setObjectName(_fromUtf8("advancedOptionsMenuItem"))
    self.actionAbout_Qt4 = QtGui.QAction(MainWindow)
    self.actionAbout_Qt4.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
    self.actionAbout_Qt4.setMenuRole(QtGui.QAction.AboutQtRole)
    self.actionAbout_Qt4.setObjectName(_fromUtf8("actionAbout_Qt4"))
    self.actionAbout_PyQt = QtGui.QAction(MainWindow)
    self.actionAbout_PyQt.setText(QtGui.QApplication.translate("MainWindow", "About PyQt", None, QtGui.QApplication.UnicodeUTF8))
    self.actionAbout_PyQt.setObjectName(_fromUtf8("actionAbout_PyQt"))
    self.actionList = QtGui.QAction(MainWindow)
    self.actionList.setCheckable(True)
    self.actionList.setChecked(True)
    self.actionList.setText(QtGui.QApplication.translate("MainWindow", "List", None, QtGui.QApplication.UnicodeUTF8))
    self.actionList.setObjectName(_fromUtf8("actionList"))
    self.actionIcon = QtGui.QAction(MainWindow)
    self.actionIcon.setCheckable(True)
    self.actionIcon.setText(QtGui.QApplication.translate("MainWindow", "Icon", None, QtGui.QApplication.UnicodeUTF8))
    self.actionIcon.setObjectName(_fromUtf8("actionIcon"))
    self.actionAdvanced_Mode = QtGui.QAction(MainWindow)
    self.actionAdvanced_Mode.setCheckable(True)
    self.actionAdvanced_Mode.setChecked(True)
    self.actionAdvanced_Mode.setText(QtGui.QApplication.translate("MainWindow", "Advanced Mode", None, QtGui.QApplication.UnicodeUTF8))
    self.actionAdvanced_Mode.setObjectName(_fromUtf8("actionAdvanced_Mode"))
    self.addPageMenuItem = QtGui.QAction(MainWindow)
    self.addPageMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Add Page", None, QtGui.QApplication.UnicodeUTF8))
    self.addPageMenuItem.setObjectName(_fromUtf8("addPageMenuItem"))
    self.removePageMenuItem = QtGui.QAction(MainWindow)
    self.removePageMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Remove Page", None, QtGui.QApplication.UnicodeUTF8))
    self.removePageMenuItem.setObjectName(_fromUtf8("removePageMenuItem"))
    self.startBindingMenuItem = QtGui.QAction(MainWindow)
    self.startBindingMenuItem.setText(QtGui.QApplication.translate("MainWindow", "Start Binding", None, QtGui.QApplication.UnicodeUTF8))
    self.startBindingMenuItem.setObjectName(_fromUtf8("startBindingMenuItem"))
    self.menuFile.addAction(self.newMenuItem)
    self.menuFile.addAction(self.openMenuItem)
    self.menuFile.addSeparator()
    self.menuFile.addAction(self.saveMenuItem)
    self.menuFile.addAction(self.saveAsMenuItem)
    self.menuFile.addSeparator()
    self.menuFile.addAction(self.quitMenuItem)
    self.menuAbout.addAction(self.helpMenuItem)
    self.menuAbout.addSeparator()
    self.menuAbout.addAction(self.aboutMenuItem)
    self.menuAbout.addAction(self.actionAbout_Qt4)
    self.menuAbout.addAction(self.actionAbout_PyQt)
    self.menuPage_Style.addAction(self.actionList)
    self.menuPage_Style.addAction(self.actionIcon)
    self.menuView.addAction(self.menuPage_Style.menuAction())
    self.menuView.addAction(self.filePreviewsMenuItem)
    self.menuPage.addAction(self.addPageMenuItem)
    self.menuPage.addAction(self.removePageMenuItem)
    self.menuBar.addAction(self.menuFile.menuAction())
    self.menuBar.addAction(self.menuEdit.menuAction())
    self.menuBar.addAction(self.menuPage.menuAction())
    self.menuBar.addAction(self.menuView.menuAction())
    self.menuBar.addAction(self.menuAbout.menuAction())
    self.toolBar.addAction(self.newMenuItem)
    self.toolBar.addAction(self.openMenuItem)
    self.toolBar.addAction(self.saveMenuItem)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.addPageMenuItem)
    self.toolBar.addAction(self.removePageMenuItem)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.startBindingMenuItem)

    self.retranslateUi(MainWindow)
    self.tabWidget.setCurrentIndex(0)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Page", None, QtGui.QApplication.UnicodeUTF8))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QtGui.QApplication.translate("MainWindow", "Book", None, QtGui.QApplication.UnicodeUTF8))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), QtGui.QApplication.translate("MainWindow", "OCR", None, QtGui.QApplication.UnicodeUTF8))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget1), QtGui.QApplication.translate("MainWindow", "DjVu Encoders", None, QtGui.QApplication.UnicodeUTF8))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("MainWindow", "Debug Log", None, QtGui.QApplication.UnicodeUTF8))

from BookListWidget import BookListWidget
from DebugLog import DebugLog
import resources_rc
