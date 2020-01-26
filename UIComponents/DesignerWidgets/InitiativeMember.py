# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InitiativeMember.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitiativeMember(object):
    def setupUi(self, InitiativeMember):
        InitiativeMember.setObjectName("InitiativeMember")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InitiativeMember.sizePolicy().hasHeightForWidth())
        InitiativeMember.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(InitiativeMember)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.initLayout = QtWidgets.QVBoxLayout()
        self.initLayout.setObjectName("initLayout")
        self.initLabel = QtWidgets.QLabel(InitiativeMember)
        self.initLabel.setObjectName("initLabel")
        self.initLayout.addWidget(self.initLabel)
        self.initNum = QtWidgets.QSpinBox(InitiativeMember)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initNum.sizePolicy().hasHeightForWidth())
        self.initNum.setSizePolicy(sizePolicy)
        self.initNum.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.initNum.setObjectName("initNum")
        self.initLayout.addWidget(self.initNum)
        self.gridLayout_2.addLayout(self.initLayout, 0, 0, 1, 1)
        self.characterLayout = QtWidgets.QVBoxLayout()
        self.characterLayout.setObjectName("characterLayout")
        self.characterLabel = QtWidgets.QLabel(InitiativeMember)
        self.characterLabel.setObjectName("characterLabel")
        self.characterLayout.addWidget(self.characterLabel)
        self.characterName = QtWidgets.QLineEdit(InitiativeMember)
        self.characterName.setObjectName("characterName")
        self.characterLayout.addWidget(self.characterName)
        self.gridLayout_2.addLayout(self.characterLayout, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(InitiativeMember)
        QtCore.QMetaObject.connectSlotsByName(InitiativeMember)

    def retranslateUi(self, InitiativeMember):
        _translate = QtCore.QCoreApplication.translate
        InitiativeMember.setWindowTitle(_translate("InitiativeMember", "Form"))
        InitiativeMember.setAccessibleName(_translate("InitiativeMember", "InitMember"))
        self.initLabel.setText(_translate("InitiativeMember", "Number"))
        self.characterLabel.setText(_translate("InitiativeMember", "Character"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InitiativeMember = QtWidgets.QWidget()
    ui = Ui_InitiativeMember()
    ui.setupUi(InitiativeMember)
    InitiativeMember.show()
    sys.exit(app.exec_())
