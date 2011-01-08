# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Fri Jan  7 23:31:33 2011
#      by: PyQt4 UI code generator 4.8.1
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
        MainWindow.resize(614, 786)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.pageList = DropListWidget(self.centralwidget)
        self.pageList.setAcceptDrops(True)
        self.pageList.setStyleSheet(_fromUtf8("QListView\n"
"{\n"
"background-image: url(\"./icons/go-down-big.png\");\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"background-color: white;\n"
"}\n"
"\n"
"QListView:hover\n"
"{\n"
"background-image: url(\"./icons/go-down-big-hover.png\");\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"background-color: white;\n"
"}"))
        self.pageList.setDragEnabled(True)
        self.pageList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.pageList.setAlternatingRowColors(True)
        self.pageList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.pageList.setIconSize(QtCore.QSize(72, 72))
        self.pageList.setMovement(QtGui.QListView.Snap)
        self.pageList.setObjectName(_fromUtf8("pageList"))
        self.verticalLayout_2.addWidget(self.pageList)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.addPageButton = QtGui.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addPageButton.setIcon(icon)
        self.addPageButton.setObjectName(_fromUtf8("addPageButton"))
        self.horizontalLayout_2.addWidget(self.addPageButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.removePageButton = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removePageButton.setIcon(icon1)
        self.removePageButton.setAutoRepeat(False)
        self.removePageButton.setFlat(False)
        self.removePageButton.setObjectName(_fromUtf8("removePageButton"))
        self.horizontalLayout_2.addWidget(self.removePageButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.enableOCR = QtGui.QCheckBox(self.centralwidget)
        self.enableOCR.setObjectName(_fromUtf8("enableOCR"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.enableOCR)
        self.ocrEngineLabel = QtGui.QLabel(self.centralwidget)
        self.ocrEngineLabel.setObjectName(_fromUtf8("ocrEngineLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.ocrEngineLabel)
        self.ocrEngine = QtGui.QComboBox(self.centralwidget)
        self.ocrEngine.setEnabled(False)
        self.ocrEngine.setObjectName(_fromUtf8("ocrEngine"))
        self.ocrEngine.addItem(_fromUtf8(""))
        self.ocrEngine.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ocrEngine)
        self.ocrOptionsLabel = QtGui.QLabel(self.centralwidget)
        self.ocrOptionsLabel.setEnabled(True)
        self.ocrOptionsLabel.setObjectName(_fromUtf8("ocrOptionsLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.ocrOptionsLabel)
        self.ocrOptions = QtGui.QLineEdit(self.centralwidget)
        self.ocrOptions.setEnabled(False)
        self.ocrOptions.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ocrOptions.setObjectName(_fromUtf8("ocrOptions"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ocrOptions)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.startButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/media-playback-start.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon2)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout_5.addWidget(self.startButton)
        self.stopButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("./icons/media-playback-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon3)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.horizontalLayout_5.addWidget(self.stopButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setEnabled(True)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(MainWindow)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionSave_as_2 = QtGui.QAction(MainWindow)
        self.actionSave_as_2.setObjectName(_fromUtf8("actionSave_as_2"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.enableOCR, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ocrOptions.setEnabled)
        QtCore.QObject.connect(self.enableOCR, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ocrEngine.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bindery", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Drop the book\'s pages below", None, QtGui.QApplication.UnicodeUTF8))
        self.addPageButton.setText(QtGui.QApplication.translate("MainWindow", "Add page", None, QtGui.QApplication.UnicodeUTF8))
        self.removePageButton.setText(QtGui.QApplication.translate("MainWindow", "Remove page", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Configure the binding options below", None, QtGui.QApplication.UnicodeUTF8))
        self.enableOCR.setText(QtGui.QApplication.translate("MainWindow", "Enable OCR", None, QtGui.QApplication.UnicodeUTF8))
        self.ocrEngineLabel.setText(QtGui.QApplication.translate("MainWindow", "OCR Engine", None, QtGui.QApplication.UnicodeUTF8))
        self.ocrEngine.setItemText(0, QtGui.QApplication.translate("MainWindow", "Tesseract", None, QtGui.QApplication.UnicodeUTF8))
        self.ocrEngine.setItemText(1, QtGui.QApplication.translate("MainWindow", "Cuniform", None, QtGui.QApplication.UnicodeUTF8))
        self.ocrOptionsLabel.setText(QtGui.QApplication.translate("MainWindow", "Engine Options", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButton.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate("MainWindow", "%p%", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setText(QtGui.QApplication.translate("MainWindow", "Save as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as_2.setText(QtGui.QApplication.translate("MainWindow", "Save as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

from DropListWidget import DropListWidget
import resources_rc
