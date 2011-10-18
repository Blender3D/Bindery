# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_files.ui'
#
# Created: Tue Oct 18 15:53:16 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class Ui_ProjectFilesDialog(object):
  def setupUi(self, ProjectFilesDialog):
    ProjectFilesDialog.setObjectName(_fromUtf8("ProjectFilesDialog"))
    ProjectFilesDialog.resize(427, 472)
    ProjectFilesDialog.setWindowTitle(QtGui.QApplication.translate("ProjectFilesDialog", "Project Files", None, QtGui.QApplication.UnicodeUTF8))
    ProjectFilesDialog.setModal(True)
    self.gridLayout = QtGui.QGridLayout(ProjectFilesDialog)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.verticalLayout_2 = QtGui.QVBoxLayout()
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.groupBox_2 = QtGui.QGroupBox(ProjectFilesDialog)
    self.groupBox_2.setTitle(QtGui.QApplication.translate("ProjectFilesDialog", "Input Directory", None, QtGui.QApplication.UnicodeUTF8))
    self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
    self.hboxlayout = QtGui.QHBoxLayout(self.groupBox_2)
    self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
    self.inputDirectory = QtGui.QLineEdit(self.groupBox_2)
    self.inputDirectory.setEnabled(True)
    self.inputDirectory.setObjectName(_fromUtf8("inputDirectory"))
    self.hboxlayout.addWidget(self.inputDirectory)
    self.browseButton1 = QtGui.QPushButton(self.groupBox_2)
    self.browseButton1.setText(QtGui.QApplication.translate("ProjectFilesDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
    self.browseButton1.setObjectName(_fromUtf8("browseButton1"))
    self.hboxlayout.addWidget(self.browseButton1)
    self.verticalLayout_2.addWidget(self.groupBox_2)
    self.groupBox = QtGui.QGroupBox(ProjectFilesDialog)
    self.groupBox.setTitle(QtGui.QApplication.translate("ProjectFilesDialog", "Output File", None, QtGui.QApplication.UnicodeUTF8))
    self.groupBox.setObjectName(_fromUtf8("groupBox"))
    self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox)
    self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
    self.outputFile = QtGui.QLineEdit(self.groupBox)
    self.outputFile.setObjectName(_fromUtf8("outputFile"))
    self.hboxlayout1.addWidget(self.outputFile)
    self.browseButton2 = QtGui.QPushButton(self.groupBox)
    self.browseButton2.setText(QtGui.QApplication.translate("ProjectFilesDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
    self.browseButton2.setObjectName(_fromUtf8("browseButton2"))
    self.hboxlayout1.addWidget(self.browseButton2)
    self.verticalLayout_2.addWidget(self.groupBox)
    self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
    self.hboxlayout2 = QtGui.QHBoxLayout()
    self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
    self.groupBox_3 = QtGui.QGroupBox(ProjectFilesDialog)
    self.groupBox_3.setTitle(QtGui.QApplication.translate("ProjectFilesDialog", "Files Not In Project", None, QtGui.QApplication.UnicodeUTF8))
    self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
    self.vboxlayout = QtGui.QVBoxLayout(self.groupBox_3)
    self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
    self.offProjectList = QtGui.QListWidget(self.groupBox_3)
    self.offProjectList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.offProjectList.setObjectName(_fromUtf8("offProjectList"))
    self.vboxlayout.addWidget(self.offProjectList)
    self.selectAllButton1 = QtGui.QPushButton(self.groupBox_3)
    self.selectAllButton1.setText(QtGui.QApplication.translate("ProjectFilesDialog", "Select All", None, QtGui.QApplication.UnicodeUTF8))
    self.selectAllButton1.setObjectName(_fromUtf8("selectAllButton1"))
    self.vboxlayout.addWidget(self.selectAllButton1)
    self.hboxlayout2.addWidget(self.groupBox_3)
    self.vboxlayout1 = QtGui.QVBoxLayout()
    self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.vboxlayout1.addItem(spacerItem)
    self.addToProjectButton = QtGui.QToolButton(ProjectFilesDialog)
    self.addToProjectButton.setToolTip(QtGui.QApplication.translate("ProjectFilesDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add selected files to project.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
    self.addToProjectButton.setText(_fromUtf8(""))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.addToProjectButton.setIcon(icon)
    self.addToProjectButton.setIconSize(QtCore.QSize(24, 24))
    self.addToProjectButton.setObjectName(_fromUtf8("addToProjectButton"))
    self.vboxlayout1.addWidget(self.addToProjectButton)
    self.removeFromProjectButton = QtGui.QToolButton(ProjectFilesDialog)
    self.removeFromProjectButton.setToolTip(QtGui.QApplication.translate("ProjectFilesDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected files from project.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
    self.removeFromProjectButton.setText(_fromUtf8(""))
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.removeFromProjectButton.setIcon(icon1)
    self.removeFromProjectButton.setIconSize(QtCore.QSize(24, 24))
    self.removeFromProjectButton.setObjectName(_fromUtf8("removeFromProjectButton"))
    self.vboxlayout1.addWidget(self.removeFromProjectButton)
    spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.vboxlayout1.addItem(spacerItem1)
    self.hboxlayout2.addLayout(self.vboxlayout1)
    self.groupBox_4 = QtGui.QGroupBox(ProjectFilesDialog)
    self.groupBox_4.setTitle(QtGui.QApplication.translate("ProjectFilesDialog", "Files In Project", None, QtGui.QApplication.UnicodeUTF8))
    self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
    self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_4)
    self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
    self.inProjectList = QtGui.QListWidget(self.groupBox_4)
    self.inProjectList.setEnabled(True)
    self.inProjectList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.inProjectList.setObjectName(_fromUtf8("inProjectList"))
    self.vboxlayout2.addWidget(self.inProjectList)
    self.selectAllButton2 = QtGui.QPushButton(self.groupBox_4)
    self.selectAllButton2.setText(QtGui.QApplication.translate("ProjectFilesDialog", "Select All", None, QtGui.QApplication.UnicodeUTF8))
    self.selectAllButton2.setObjectName(_fromUtf8("selectAllButton2"))
    self.vboxlayout2.addWidget(self.selectAllButton2)
    self.hboxlayout2.addWidget(self.groupBox_4)
    self.gridLayout.addLayout(self.hboxlayout2, 1, 0, 1, 1)
    self.verticalLayout_3 = QtGui.QVBoxLayout()
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem2)
    self.cancelButton = QtGui.QPushButton(ProjectFilesDialog)
    self.cancelButton.setText(QtGui.QApplication.translate("ProjectFilesDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
    self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
    self.horizontalLayout.addWidget(self.cancelButton)
    self.okButton = QtGui.QPushButton(ProjectFilesDialog)
    self.okButton.setText(QtGui.QApplication.translate("ProjectFilesDialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))
    self.okButton.setDefault(True)
    self.okButton.setObjectName(_fromUtf8("okButton"))
    self.horizontalLayout.addWidget(self.okButton)
    self.verticalLayout_3.addLayout(self.horizontalLayout)
    self.gridLayout.addLayout(self.verticalLayout_3, 2, 0, 1, 1)

    self.retranslateUi(ProjectFilesDialog)
    QtCore.QObject.connect(self.selectAllButton1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.offProjectList.selectAll)
    QtCore.QObject.connect(self.selectAllButton2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.inProjectList.selectAll)
    QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ProjectFilesDialog.reject)
    QtCore.QMetaObject.connectSlotsByName(ProjectFilesDialog)

  def retranslateUi(self, ProjectFilesDialog):
    self.offProjectList.setSortingEnabled(True)
    self.inProjectList.setSortingEnabled(True)

import resources_rc
