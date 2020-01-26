# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpellItem.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_spellItem(object):
    def setupUi(self, spellItem):
        spellItem.setObjectName("spellItem")
        spellItem.resize(400, 29)
        self.horizontalLayout = QtWidgets.QHBoxLayout(spellItem)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spellPrepared = QtWidgets.QCheckBox(spellItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spellPrepared.sizePolicy().hasHeightForWidth())
        self.spellPrepared.setSizePolicy(sizePolicy)
        self.spellPrepared.setText("")
        self.spellPrepared.setObjectName("spellPrepared")
        self.horizontalLayout.addWidget(self.spellPrepared)
        self.spell = QtWidgets.QLineEdit(spellItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spell.sizePolicy().hasHeightForWidth())
        self.spell.setSizePolicy(sizePolicy)
        self.spell.setMinimumSize(QtCore.QSize(0, 10))
        self.spell.setObjectName("spell")
        self.horizontalLayout.addWidget(self.spell)

        self.retranslateUi(spellItem)
        QtCore.QMetaObject.connectSlotsByName(spellItem)

    def retranslateUi(self, spellItem):
        _translate = QtCore.QCoreApplication.translate
        spellItem.setWindowTitle(_translate("spellItem", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    spellItem = QtWidgets.QWidget()
    ui = Ui_spellItem()
    ui.setupUi(spellItem)
    spellItem.show()
    sys.exit(app.exec_())
