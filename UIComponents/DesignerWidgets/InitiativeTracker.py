# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InitiativeTracker.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitTracker(object):
    def setupUi(self, InitTracker):
        InitTracker.setObjectName("InitTracker")
        InitTracker.resize(287, 368)
        self.gridLayout = QtWidgets.QGridLayout(InitTracker)
        self.gridLayout.setObjectName("gridLayout")
        self.overallLayout = QtWidgets.QVBoxLayout()
        self.overallLayout.setObjectName("overallLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addButton = QtWidgets.QPushButton(InitTracker)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.deleteSelected = QtWidgets.QPushButton(InitTracker)
        self.deleteSelected.setObjectName("deleteSelected")
        self.horizontalLayout_2.addWidget(self.deleteSelected)
        self.deleteAll = QtWidgets.QToolButton(InitTracker)
        self.deleteAll.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Icons/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteAll.setIcon(icon)
        self.deleteAll.setObjectName("deleteAll")
        self.horizontalLayout_2.addWidget(self.deleteAll)
        self.overallLayout.addLayout(self.horizontalLayout_2)
        self.initList = QtWidgets.QListWidget(InitTracker)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initList.sizePolicy().hasHeightForWidth())
        self.initList.setSizePolicy(sizePolicy)
        self.initList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.initList.setObjectName("initList")
        self.overallLayout.addWidget(self.initList)
        self.gridLayout.addLayout(self.overallLayout, 0, 0, 1, 1)

        self.retranslateUi(InitTracker)
        QtCore.QMetaObject.connectSlotsByName(InitTracker)

    def retranslateUi(self, InitTracker):
        _translate = QtCore.QCoreApplication.translate
        InitTracker.setWindowTitle(_translate("InitTracker", "Form"))
        self.addButton.setText(_translate("InitTracker", "+"))
        self.deleteSelected.setText(_translate("InitTracker", "-"))
from .resource_icons_rc import *


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InitTracker = QtWidgets.QWidget()
    ui = Ui_InitTracker()
    ui.setupUi(InitTracker)
    InitTracker.show()
    sys.exit(app.exec_())
